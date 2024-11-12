from jinja2 import Environment, FileSystemLoader
import uuid
import os
from code_generation.utilities import to_valid_variable_name


def prepare_deployment_data(order, components):
    component_mapping = {comp['metadata']['name']: comp for comp in components}
    deployment_data = []
    name_to_variable = {}

    def create_service_data(node_name, service_name, component):
        mapped = []
        if 'ports' in component:
            mapped = dict(map(lambda x: x.values(), component['ports']['required']['strong']))
        return {
            "node_name": node_name,
            "service_name": service_name,
            "variable_name": f"{service_name}",
            "image": component['spec']['template']['spec']['containers'][0]['image'],
            "cpu": component['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'],
            "memory": component['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'],
            "depends_on": [{"service_name": name_to_variable[k][:mapped[k]]} for k in mapped]
        }
    service_group = []
    for node_name, service_name in order:
        if service_name not in name_to_variable:
            name_to_variable[service_name] = []
        service_props = component_mapping[service_name]
        variable_name = service_name + '_' + to_valid_variable_name(str(uuid.uuid4()))
        service_data = create_service_data(
            node_name=node_name,
            service_name=variable_name,
            component=service_props
        )
        name_to_variable[service_name] += [variable_name]
        service_group.append(service_data)
    deployment_data.append(service_group)

    return deployment_data


def generate_python_script(order, components, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    file_loader = FileSystemLoader('script_template')
    env = Environment(loader=file_loader)
    template = env.get_template('orchestration_program.jinja2')

    increase_name = f"increase-{uuid.uuid4()}"
    project_name = f"pulumi-k8s-{folder_name}-{increase_name}"
    deployment_data = prepare_deployment_data(order, components)
    rendered_script = template.render(
        deployment_data=deployment_data,
        increase_name=increase_name,
        project_name=project_name
    )

    with open(f"{folder_name}/pulumi_deployment.py", 'w') as f:
        f.write(rendered_script)


