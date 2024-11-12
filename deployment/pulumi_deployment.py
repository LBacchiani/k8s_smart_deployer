import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    pod_backend_0 = k8s.core.v1.Pod("pod_backend_0",
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
            "nodeName": "backend"
        }
        
    )
        
    

    # Export pod names
    
        
    pulumi.export("pod_backend_0_name", pod_backend_0.metadata["name"])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name="increase-4150c1ad-bbcb-407d-a3a0-7b48f128ecaa",
        project_name="pulumi-k8s-./deployment-increase-4150c1ad-bbcb-407d-a3a0-7b48f128ecaa",
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

    
        
    print(f"Pod backend-0 Name: {up_res.outputs['pod_backend_0_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name="increase-4150c1ad-bbcb-407d-a3a0-7b48f128ecaa",
        project_name="pulumi-k8s-./deployment-increase-4150c1ad-bbcb-407d-a3a0-7b48f128ecaa",
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
        deploy_orchestration()