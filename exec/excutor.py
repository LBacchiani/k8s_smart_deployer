import subprocess
import shutil
from pathlib import Path
from enum import Enum
import tempfile

Op = Enum("Op", [("DEPLOY", "deploy"), ("DESTROY", "destroy")])
def execute_python(file_path: str, operation: str):
    converted_path = Path(file_path)
    ensure_path(converted_path)
    check_file_extension(converted_path, ".py")
    ensure_operation_exists(operation)

    try:
        if operation == Op.DEPLOY.value:
            subprocess.run(["python", str(file_path)], check=True)
        elif operation == Op.DESTROY.value:
            subprocess.run(["python", str(file_path), "destroy"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}")

def execute_yaml(file_path: str, operation: str):
    converted_file_path = Path(file_path)
    ensure_path(converted_file_path)
    check_file_extension(converted_file_path, ".yaml")
    ensure_operation_exists(operation)

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)


            subprocess.run(["pulumi", "new", "yaml", "-y"], cwd=temp_dir_path, check=True)
            default_stack_name = "dev"

            destination = temp_dir_path / "Pulumi.yaml"
            shutil.copy(converted_file_path, destination)

            command = "up" if operation == Op.DEPLOY.value else "destroy"

            out = subprocess.run(
                ["pulumi", command, "-f", "-y", "--stack", default_stack_name],
                cwd=temp_dir_path,
                capture_output=True,
                text=True,
                check=True,
            )

    except subprocess.CalledProcessError as e:
        print(f"Pulumi command failed: {e}")
        print("Error output:", e.stderr)

def execute(file_path: str, operation: str):
    """
    Executes the appropriate function (execute_python or execute_yaml)
    based on the file extension of the provided file_path.
    """
    file_extension = Path(file_path).suffix

    if file_extension == ".py":
        execute_python(file_path, operation)
    elif file_extension == ".yaml":
        execute_yaml(file_path, operation)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported types are .py and .yaml.")

def ensure_operation_exists(operation: str):
    if operation not in Op:
        raise ValueError(f"Operation {operation} is not supported.")

def ensure_path(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

def check_file_extension(file_path: Path, extension: str):
    if not file_path.suffix == extension:
        raise ValueError(f"File {file_path} is not of the correct type, it should be {extension}.")