import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    pod_proxy_0 = k8s.core.v1.Pod("pod-proxy-0",
        metadata={
            "name": f"pod-proxy-0",
        },
        spec={
            "containers": [
                {
                    "name": "proxy-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "450m",
                            "memory": "600M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-0"
        }
        
    )
        
    pod_proxy_1 = k8s.core.v1.Pod("pod-proxy-1",
        metadata={
            "name": f"pod-proxy-1",
        },
        spec={
            "containers": [
                {
                    "name": "proxy-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "450m",
                            "memory": "600M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-0"
        }
        
    )
        
    
        
    pod_backend_0 = k8s.core.v1.Pod("pod-backend-0",
        metadata={
            "name": f"pod-backend-0",
        },
        spec={
            "containers": [
                {
                    "name": "backend-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-1"
        }
        
        ,opts=pulumi.ResourceOptions(depends_on=[

                pod_proxy_0,
                pod_proxy_1,
            
        ])
        
    )
        
    pod_backend_1 = k8s.core.v1.Pod("pod-backend-1",
        metadata={
            "name": f"pod-backend-1",
        },
        spec={
            "containers": [
                {
                    "name": "backend-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-1"
        }
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                pod_proxy_0,
            
                pod_proxy_1,
            
        ])
        
    )
        
    pod_backend_2 = k8s.core.v1.Pod("pod-backend-2",
        metadata={
            "name": f"pod-backend-2",
        },
        spec={
            "containers": [
                {
                    "name": "backend-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-1"
        }
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                pod_proxy_0,
            
                pod_proxy_1,
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export("pod_proxy_0_name", pod_proxy_0.metadata["name"])
        
    pulumi.export("pod_proxy_1_name", pod_proxy_1.metadata["name"])
        
    
        
    pulumi.export("pod_backend_0_name", pod_backend_0.metadata["name"])
        
    pulumi.export("pod_backend_1_name", pod_backend_1.metadata["name"])
        
    pulumi.export("pod_backend_2_name", pod_backend_2.metadata["name"])
        
    

def deploy_pods_on_specific_node():
    stack = auto.create_or_select_stack(
        stack_name="dev-1",
        project_name="k8s-pods-on-specific-node",
        program=pulumi_program
    )

    print("Successfully initialized stack")

    kubeconfig_path = os.getenv('KUBECONFIG', '~/.kube/config')
    print(f"Using kubeconfig: {kubeconfig_path}")

    print("Refreshing stack...")
    stack.refresh(on_output=print)

    print("Previewing changes...")
    preview = stack.preview(on_output=print)

    print("Deploying changes...")
    up_res = stack.up(on_output=print)

    
        
    print(f"Pod proxy-0 Name: {up_res.outputs['pod_proxy_0_name'].value}")
        
    print(f"Pod proxy-1 Name: {up_res.outputs['pod_proxy_1_name'].value}")
        
    
        
    print(f"Pod backend-0 Name: {up_res.outputs['pod_backend_0_name'].value}")
        
    print(f"Pod backend-1 Name: {up_res.outputs['pod_backend_1_name'].value}")
        
    print(f"Pod backend-2 Name: {up_res.outputs['pod_backend_2_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name="dev-1",
        project_name="k8s-pods-on-specific-node",
        program=lambda: None
    )

    print("Destroying resources...")
    stack.destroy(on_output=print)
    print("Resources successfully destroyed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "destroy":
       destroy_pods()
    else:
        deploy_pods_on_specific_node()