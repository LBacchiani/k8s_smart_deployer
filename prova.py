import yaml

# Sample input data (could come from a file or another source)
resources = {
    "backend__4b11e1fb_83f2_4759_ac39_4c83a0c173a1": {
        "name": "backend__4b11e1fb_83f2_4759_ac39_4c83a0c173a1",
        "options": {
            "dependsOn": ["${proxy__8a5e5c89_da35_4d85_a626_a9a175a4de84}"]
        },
        "properties": {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "labels": {"app": "backend"},
                "name": "backend"
            },
            "spec": {
                "containers": [
                    {
                        "image": "k8s.gcr.io/pause:2.0",
                        "name": "backend-container",
                        "resources": {
                            "requests": {"cpu": "300m", "memory": "500M"}
                        }
                    }
                ],
                "nodeName": "k3d-k3s-default-agent-1"
            }
        },
        "type": "kubernetes:core/v1:Pod"
    },
    "proxy__8a5e5c89_da35_4d85_a626_a9a175a4de84": {
        "name": "proxy__8a5e5c89_da35_4d85_a626_a9a175a4de84",
        "options": {},
        "properties": {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "labels": {"app": "proxy"},
                "name": "proxy"
            },
            "spec": {
                "containers": [
                    {
                        "image": "k8s.gcr.io/pause:2.0",
                        "name": "proxy-container",
                        "resources": {
                            "requests": {"cpu": "450m", "memory": "600M"}
                        }
                    }
                ],
                "nodeName": "k3d-k3s-default-agent-1"
            }
        },
        "type": "kubernetes:core/v1:Pod"
    },
    "proxy_f33709e0_92b5_4180_84d8_aac9b6a589cc": {
        "name": "proxy_f33709e0_92b5_4180_84d8_aac9b6a589cc",
        "options": {},
        "properties": {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "labels": {"app": "proxy"},
                "name": "proxy"
            },
            "spec": {
                "containers": [
                    {
                        "image": "k8s.gcr.io/pause:2.0",
                        "name": "proxy-container",
                        "resources": {
                            "requests": {"cpu": "450m", "memory": "600M"}
                        }
                    }
                ],
                "nodeName": "k3d-k3s-default-agent-0"
            }
        },
        "type": "kubernetes:core/v1:Pod"
    },
    # More backend resources can go here
}

# Function to resolve dependencies and enforce proxy-first order
def resolve_dependencies(resources):
    sorted_resources = []
    visited = set()

    def visit(resource):
        if resource in visited:
            return
        visited.add(resource)

        # Ensure the resource exists in the dictionary
        if resource not in resources:
            raise KeyError(f"Resource '{resource}' not found in resources dictionary.")

        # Resolve any dependencies
        if 'dependsOn' in resources[resource]["options"]:
            for dep in resources[resource]["options"]["dependsOn"]:
                dep_resource = dep.strip("${}")  # Remove any "${}"
                visit(dep_resource)

        # Add the resource to the sorted list after resolving its dependencies
        sorted_resources.append(resource)

    # First, ensure proxy resources are visited first
    for resource in resources:
        if "proxy" in resource:  # Prioritize proxy resources
            visit(resource)

    # Then visit backend resources (or any remaining)
    for resource in resources:
        if "proxy" not in resource:  # Only backend resources here
            visit(resource)

    return sorted_resources

# Sorting resources
sorted_resource_keys = resolve_dependencies(resources)

# Rebuild the sorted YAML structure
sorted_resources = {key: resources[key] for key in sorted_resource_keys}

# Output the YAML, manually specifying the order
yaml_output = yaml.dump({
    "name": "my-k8s-app",
    "resources": sorted_resources,
    "runtime": "yaml"
}, default_flow_style=False)

# Print or save the result
print(yaml_output)
