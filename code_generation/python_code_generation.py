from jinja2 import Environment, FileSystemLoader
import yaml
import re
import uuid
import os


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def to_valid_variable_name(input_string: str) -> str:
    cleaned_string = re.sub(r'[^0-9a-zA-Z_]', '_', input_string)

    if not cleaned_string[0].isalpha() and cleaned_string[0] != '_':
        cleaned_string = f'_{cleaned_string}'

    return cleaned_string

def prepare_deployment_data(order, components, excluded_services):

    component_mapping = {comp['metadata']['name']: comp for comp in components}
    deployment_data = []
    deployed_services = []

    def create_service_data(node_name, service_name, service_index, component):
        return {
            "node_name": node_name,
            "service_name": service_name,
            "variable_name": to_valid_variable_name(f"pod_{service_name}_{service_index}"),
            "service_index": service_index,
            "image": component['spec']['template']['spec']['containers'][0]['image'],
            "cpu": component['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'],
            "memory": component['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'],
            "depends_on": [
                {"service_name": dep_service["service_name"], "service_index": dep_service["service_index"]}
                for dep_service in deployed_services
            ]
        }

    if not order:
        for component in components:
            service_name = component['metadata']['name']
            if service_name not in excluded_services:
                service_data = create_service_data(
                    node_name=service_name,
                    service_name=service_name,
                    service_index=0,
                    component=component
                )
                deployment_data.append([service_data])
        return deployment_data

    for service_info_set in order:
        service_group = []
        for service_info in service_info_set:
            node_name = service_info[0]
            service_name = service_info[2]
            service_index = service_info[3]

            if service_name not in excluded_services:
                component = component_mapping.get(service_name)
                if component:
                    service_data = create_service_data(
                        node_name=node_name,
                        service_name=service_name,
                        service_index=service_index,
                        component=component
                    )
                    service_group.append(service_data)

        deployment_data.append(service_group)
        deployed_services.extend(service_group)

    return deployment_data


def generate_python_script(order, components, folder_name, excluded_services=None):
    if excluded_services is None:
        excluded_services = {}

    os.makedirs(folder_name, exist_ok=True)
    file_loader = FileSystemLoader('script_template')
    env = Environment(loader=file_loader)
    template = env.get_template('orchestration_program.jinja2')

    increase_name = f"increase-{uuid.uuid4()}"
    project_name = f"pulumi-k8s-{folder_name}-{increase_name}"
    deployment_data = prepare_deployment_data(order, components, excluded_services)
    rendered_script = template.render(
        deployment_data=deployment_data,
        increase_name=increase_name,
        project_name=project_name
    )

    with open(f"{folder_name}/pulumi_deployment.py", 'w') as f:
        f.write(rendered_script)


