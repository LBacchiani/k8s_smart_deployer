import yaml
import os

def generate_yaml(node_name, service_name, config_file, replicas):
    os.makedirs("deployments", exist_ok=True)
    file_name = "deployments/" + node_name + "_" + service_name + ".yaml"
    config_file['spec']['replicas'] = replicas
    clean_config(config_file['spec']['template']['spec'], "affinity")
    clean_config(config_file['spec']['template']['spec'], "schedulerName")
    config_file['spec']['template']['spec']['nodeName'] = node_name
    with open(file_name, "w") as file: yaml.dump(config_file, file)

def clean_config(config, to_remove):
    if to_remove in config:
        config.pop(to_remove)