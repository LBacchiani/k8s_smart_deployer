import subprocess
import shutil
from pathlib import Path
from enum import Enum
from kubernetes import client, config
from typing import Dict, List
import yaml
import ast

Op = Enum("Op", [("DEPLOY", "deploy"), ("DESTROY", "destroy")])
def execute_python(file_path: str, stack_name: str, operation: str, mapping:  Dict[str, List[str]]):
    converted_path = Path(file_path)
    ensure_path(converted_path)
    check_file_extension(converted_path, ".py")
    ensure_operation_exists(operation)

    substitute_env_types_in_python(converted_path, mapping)

    try:
        if operation == Op.DEPLOY.value:
            subprocess.run(["python", file_path, stack_name], check=True)
        elif operation == Op.DESTROY.value:
            subprocess.run(["python", file_path, stack_name, "destroy"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}")

def execute_yaml(file_path: str, stack_name:str, operation: str, project_path: str, mapping:  Dict[str, List[str]]):
    converted_file_path = Path(file_path)
    converted_project_path = Path(project_path)
    ensure_path(converted_file_path)
    check_file_extension(converted_file_path, ".yaml")
    ensure_operation_exists(operation)
    
    try:
        destination = converted_project_path / "Pulumi.yaml"
        shutil.copy(converted_file_path, destination)

        substitute_env_types_in_yaml(destination, mapping)

        command = "up" if operation == Op.DEPLOY.value else "destroy"

        out_select_stack = subprocess.run(
            ["pulumi", "stack", "select", "--non-interactive", "-c", stack_name],
            cwd=converted_project_path,
            check=True
        )

        print(out_select_stack)

        out_up_command = subprocess.run(
            ["pulumi", command, "-f", "-y", "--non-interactive", "--stack", stack_name],
            cwd=converted_project_path,
            capture_output=True,
            text=True,
        )

        print(out_up_command.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Pulumi command failed: {e}")
        print("Error output:", e.stderr)

def execute(file_path: str, stack_name:str, operation: str, project_path: str):
    """
    Executes the appropriate function (execute_python or execute_yaml)
    based on the file extension of the provided file_path.
    """
    file_extension = Path(file_path).suffix
    mappings = map_services_by_type(in_cluster=False)
    print(mappings)

    if file_extension == ".py":
        execute_python(file_path, stack_name, operation, mappings)
    elif file_extension == ".yaml":
        execute_yaml(file_path, stack_name, operation, project_path, mappings)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported types are .py and .yaml.")

def ensure_operation_exists(operation: str):
    allowed = {op.value for op in Op}
    if operation not in allowed:
        raise ValueError(f"Operation {operation!r} is not supported.  Choose one of {sorted(allowed)}")

def ensure_path(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

def check_file_extension(file_path: Path, extension: str):
    if not file_path.suffix == extension:
        raise ValueError(f"File {file_path} is not of the correct type, it should be {extension}.")

def map_services_by_type(in_cluster: bool = False) -> Dict[str, List[str]]:
    if in_cluster:
        config.load_incluster_config()
    else:
        config.load_kube_config()

    v1 = client.CoreV1Api()
    
    services = v1.list_service_for_all_namespaces().items

    type_map: Dict[str, List[str]] = {}
    
    for svc in services:
        name = svc.metadata.name
        labels = svc.metadata.labels or {}
        print(name, labels)
        svc_type = labels.get("type")
        if not svc_type:
            continue
        
        type_map.setdefault(svc_type, []).append(name)

    return type_map

def substitute_env_types_in_yaml(yaml_path: Path, mapping: Dict[str, List[str]]):
    data = yaml.safe_load(yaml_path.read_text())

    for res in data.get("resources", {}).values():
        props = res.get("properties", {})
        spec  = props.get("spec", {})
        for container in spec.get("containers", []):
            for env in container.get("env", []):
                if "type" in env:
                    type_key = env.pop("type")
                    if type_key not in mapping or not mapping[type_key]:
                        raise KeyError(f"No mapping for env type '{type_key}'")
                    env["value"] = mapping[type_key][0]

    yaml_path.write_text(yaml.safe_dump(data, sort_keys=False))

def substitute_env_types_in_python(py_path: Path, mapping: Dict[str, List[str]]):

    source = py_path.read_text()
    tree = ast.parse(source)

    class EnvTypeRewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST:
            func = node.func
            is_envvar = False
            if isinstance(func, ast.Attribute) and func.attr == "EnvVarArgs":
                is_envvar = True
            elif isinstance(func, ast.Name) and func.id == "EnvVarArgs":
                is_envvar = True

            if is_envvar:
                new_kwargs = []
                for kw in node.keywords:
                    if kw.arg == "type":
                        if not (isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str)):
                            raise ValueError(f"Expected a string literal for 'type', got {ast.dump(kw.value)}")
                        type_key = kw.value.value
                        if type_key not in mapping or not mapping[type_key]:
                            raise KeyError(f"No mapping entry for env-var type '{type_key}'")
                        new_kwargs.append(ast.keyword(
                            arg="value",
                            value=ast.Constant(mapping[type_key][0])
                        ))
                    else:
                        new_kwargs.append(kw)
                node.keywords = new_kwargs

            return self.generic_visit(node)

    new_tree = EnvTypeRewriter().visit(tree)
    ast.fix_missing_locations(new_tree)

    new_source = ast.unparse(new_tree)
    py_path.write_text(new_source)