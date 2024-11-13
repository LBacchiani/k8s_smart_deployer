import subprocess
import shutil
from pathlib import Path
from enum import Enum

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


def execute_yaml(file_path: str, project_path: str, stack_name: str, operation: str):
    converted_file_path = Path(file_path)
    converted_project_path = Path(project_path)

    ensure_path(converted_file_path)
    ensure_path(converted_project_path)

    destination = converted_project_path / "Pulumi.yaml"
    shutil.copy(converted_file_path, destination)

    try:
        command = "up" if operation == Op.DEPLOY.value else "destroy"
        print(command)
        result = subprocess.run(
            ["pulumi", command, "-f", "-y", "--stack", stack_name],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Pulumi command failed: {e}")
        print("Error output:", e.stderr)

def ensure_operation_exists(operation: str):
    if operation not in Op:
        raise ValueError(f"Operation {operation} is not supported.")

def ensure_path(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

def check_file_extension(file_path: Path, extension: str):
    if not file_path.suffix == extension:
        raise ValueError(f"File {file_path} is not of the correct type, it should be {extension}.")