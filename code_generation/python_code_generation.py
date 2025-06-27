from jinja2 import Environment, FileSystemLoader
import uuid
import os
from code_generation.utilities import to_valid_variable_name, to_dns_name
from utilities import *


def prepare_deployment_data(order, components): 
    component_mapping = {refine_name(comp['metadata']['labels']['type']): comp for comp in components}
    deployment_data = []
    name_to_variable = {}

    def create_service_data(node_name, service_name, component):
        mapped = []
        if 'ports' in component:
            mapped = {
                item['type']: [item['value']]
                for item in component['ports']['required']['strong']
            }
        if component['kind'] == 'Pod':
            output = {
                "node_name": node_name,
                "kind": "Pod",
                "service_name": service_name,
                "service_label": component['metadata']['labels'],
                "variable_name": to_valid_variable_name(service_name),
                "image": component['spec']['containers'][0]['image'],
                "image_name": to_dns_name(component['spec']['containers'][0]['image']),
                "cpu": component['spec']['containers'][0]['resources']['requests']['cpu'],
                "memory": component['spec']['containers'][0]['resources']['requests']['memory'],
                "env": component['spec']['containers'][0].get('env', []),
                "depends_on": [{"service_name": name_to_variable[k][:mapped[k][0]]} for k in mapped]
            }
            return output
        elif component['kind'] == 'Service':
            result = {
                "node_name": node_name,
                "kind": "Service",
                "service_name": service_name,
                "service_label": component['metadata']['labels'],
                "metadata": component['metadata'],
                "variable_name": to_valid_variable_name(service_name),
                "selector": component['spec']['selector'],
                "ports": component['spec']['ports'],
                "depends_on": [{"service_name": name_to_variable[k][:mapped[k][0]]} for k in mapped]
            }
            if "type" in component['spec']:
                result["type"] = component['spec']['type']
            return result
    
    def bind_ports(component, deployment_data):
        if 'ports' not in component:
            return
        
        strong_port_data = component['ports']['required']['strong']
        ports_value = [ item['type'] for item in strong_port_data]
        id_type_map = {item['id']: item['type'] for item in strong_port_data if 'id' in item}

        ports_to_gen_names = {}
        for data in deployment_data:
            for deployment in data:
                kind = deployment["kind"]
                if kind != "Service": 
                    continue
                name = deployment['metadata']['labels']['type']

                for port_name in ports_value:
                    if name == port_name and name not in ports_to_gen_names:
                        ports_to_gen_names[name] = deployment['service_name']
       
        for data in deployment_data:
            for deployment in data:
                kind = deployment["kind"]
                if kind != "Pod": 
                    continue 
                for id_val, type_val in id_type_map.items():
                    if type_val in ports_to_gen_names:
                        value = ports_to_gen_names[type_val]
                        deployment['env'].append({"name": id_val, "value": value})

    service_group = []
    for node_name, service_type in order:
        generated_name = f"{service_type}-{uuid.uuid4()}".replace("-type", "")
        if service_type not in name_to_variable:
            name_to_variable[service_type] = []
        service_props = component_mapping[refine_name(service_type)]
        service_data = create_service_data(
            node_name=node_name,
            service_name=generated_name,
            component=service_props
        )

        name_to_variable[service_type] += [to_valid_variable_name(generated_name)]
        service_group.append(service_data)
    deployment_data.append(service_group)
    for _, service_type in order:
        component = component_mapping[refine_name(service_type)]
        bind_ports(component, deployment_data)

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


