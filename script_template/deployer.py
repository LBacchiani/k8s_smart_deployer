import os
import subprocess
import sys
import argparse

def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def import_required_libraries():
    try:
        global client, config, utils
        import kubernetes.client as client
        import kubernetes.config as config
        print("Kubernetes client imported successfully.")
    except ImportError:
        print("Kubernetes client not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kubernetes"])
        import kubernetes.client as client
        import kubernetes.config as config

    try:
        global yaml
        import yaml
        print("PyYAML imported successfully.")
    except ImportError:
        print("PyYAML not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        import yaml


def find_manifest_files(manifest_folder):
    manifests = []
    if not os.path.exists(manifest_folder):
        print(f"Manifest folder {manifest_folder} does not exist.")
        return manifests

    for file in os.listdir(manifest_folder):
        if file.endswith(".yaml") or file.endswith(".yml"):
            manifests.append(os.path.join(manifest_folder, file))

    return manifests


def deploy_manifests(manifest_files, namespace="default"):
    if not manifest_files:
        print("No manifest files found to deploy.")
        return []

    config.load_kube_config()
    api_client = client.ApiClient()

    deployed_pods = []
    for manifest in manifest_files:
        try:
            from kubernetes.utils import create_from_yaml
            resources = create_from_yaml(api_client, manifest, namespace=namespace)
            name = resources[0][0].metadata.name
            deployed_pods.append(name)

        except Exception as e:
             print(f"Error deploying manifest {manifest}: {e}")

    return deployed_pods

def remove_pods(pod_names, namespace="default"):
    if not pod_names:
        print("No deployed pods to remove.")
        return

    config.load_kube_config()
    api_instance = client.CoreV1Api()

    for pod_name in pod_names:
        try:
            api_instance.delete_namespaced_pod(name=pod_name, namespace=namespace)
            print(f"Pod {pod_name} deleted.")
        except Exception as e:
            print(f"Error deleting pod {pod_name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kubernetes Manifest Deployment/Pod Removal Script")

    parser.add_argument(
        "action",
        choices=["deploy", "remove"],
        help="Action to perform: 'deploy' to deploy manifests, 'remove' to remove deployed pods."
    )

    parser.add_argument(
        "--manifest-folder",
        type=str,
        default="./manifests",  # Set your default folder
        help="The folder containing the manifest YAML files (used in deploy action)."
    )

    parser.add_argument(
        "--deployed-pods-file",
        type=str,
        default="deployed_pods.txt",
        help="File to store the names of the deployed pods (used for tracking removal)."
    )

    args = parser.parse_args()
    import_required_libraries()
    if args.action == "deploy":
        manifests = find_manifest_files(args.manifest_folder)
        deployed_pods = deploy_manifests(manifests)
        with open(args.deployed_pods_file, "w") as f:
            for pod in deployed_pods:
                f.write(pod + "\n")

        print(f"Deployed pods saved to {args.deployed_pods_file}")

    elif args.action == "remove":
        try:
            with open(args.deployed_pods_file, "r") as f:
                deployed_pods = [line.strip() for line in f.readlines()]
                os.remove(args.deployed_pods_file)
        except FileNotFoundError:
            print(f"No file {args.deployed_pods_file} found. Make sure you deployed pods first.")
            sys.exit(1)

        remove_pods(deployed_pods)
