from jinja2 import Environment, FileSystemLoader
import uuid
import os
from code_generation.utilities import to_valid_variable_name, to_dns_name
from utilities import *


def prepare_deployment_data(order, components):
    component_mapping = {refine_name(comp['metadata']['name']): comp for comp in components}
    deployment_data = []
    name_to_variable = {}

    def create_service_data(node_name, service_name, component):
        mapped = []
        if 'ports' in component:
            mapped = dict(map(lambda x: x.values(), component['ports']['required']['strong']))
        if component['kind'] == 'Pod':
            return {
                "node_name": node_name,
                "kind": "Pod",
                "service_name": service_name,
                "service_label": component['metadata']['labels'],
                "variable_name": to_valid_variable_name(service_name),
                "image": component['spec']['containers'][0]['image'],
                "image_name": to_dns_name(component['spec']['containers'][0]['image']),
                "cpu": component['spec']['containers'][0]['resources']['requests']['cpu'],
                "memory": component['spec']['containers'][0]['resources']['requests']['memory'],
                "depends_on": [{"service_name": name_to_variable[k][:mapped[k]]} for k in mapped]
            }
        elif component['kind'] == 'Service':
            return {
                "node_name": node_name,
                "kind": "Service",
                "type": component['spec']['type'],
                "service_name": service_name,
                "variable_name": to_valid_variable_name(service_name),
                "selector": component['spec']['selector'],
                "ports": component['spec']['ports'],
                "depends_on": [{"service_name": name_to_variable[k][:mapped[k]]} for k in mapped]
            }
             
        
    service_group = []
    for node_name, service_name in order:
        uuid_var = str(uuid.uuid4())
        tmp_name = service_name.replace('_','-')
        if service_name not in name_to_variable:
            name_to_variable[service_name] = []
        service_props = component_mapping[refine_name(service_name)]
        gen_service_name = f"{tmp_name.replace('_','-')}-{uuid_var}" if service_props['kind'] == 'Pod' else tmp_name
        service_data = create_service_data(
            node_name=node_name,
            service_name=gen_service_name,
            component=service_props
        )
        name_to_variable[service_name] += [to_valid_variable_name(gen_service_name)]
        service_group.append(service_data)
    deployment_data.append(service_group)

    return deployment_data


def generate_python_script(order, components, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    file_loader = FileSystemLoader('script_template')
    env = Environment(loader=file_loader)
    template = env.get_template('orchestration_program.jinja2')

    increase_name = f"increase-{uuid.uuid4()}"
    project_name = f"pulumi-k8s-{increase_name}"
    deployment_data = prepare_deployment_data(order, components)
    rendered_script = template.render(
        deployment_data=deployment_data,
        increase_name=increase_name,
        project_name=project_name
    )

    with open(f"{folder_name}/pulumi_deployment.py", 'w') as f:
        f.write(rendered_script)


