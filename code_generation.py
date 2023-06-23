import yaml
import os

def generate_yaml(node_name, service_name, config_file, replicas):
    os.makedirs("deployments", exist_ok=True)
    file_name = "deployments/"+ node_name + "_" +service_name + ".yaml"
    clean_config(config_file['spec']['template']['spec']['containers'], "resources")
    data = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": service_name
        },
        "spec": {
            "selector": {
                "matchLabels": {
                    "app": service_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": service_name
                    }
                },
                "spec": {
                    "containers": config_file['spec']['template']['spec']['containers'],
                    "nodeName": node_name
                }
            },
            "replicas": replicas
        }
    }

    with open(file_name, "w") as file: yaml.dump(data, file)

def clean_config(config, to_remove):
    for data in config:
        if to_remove in data:
            del data[to_remove]