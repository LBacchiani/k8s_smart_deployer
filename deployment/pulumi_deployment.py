import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e_0 = k8s.core.v1.Pod("backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e_0",
        metadata={
            "name": f"backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e-0",
        },
        spec={
            "containers": [
                {
                    "name": "backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-0"
        }
        
    )
        
    backend__45a18026_1ab4_4e40_879d_a2c613be709c_1 = k8s.core.v1.Pod("backend__45a18026_1ab4_4e40_879d_a2c613be709c_1",
        metadata={
            "name": f"backend__45a18026_1ab4_4e40_879d_a2c613be709c-1",
        },
        spec={
            "containers": [
                {
                    "name": "backend__45a18026_1ab4_4e40_879d_a2c613be709c-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-0"
        }
        
    )
        
    backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b_0 = k8s.core.v1.Pod("backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b_0",
        metadata={
            "name": f"backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b-0",
        },
        spec={
            "containers": [
                {
                    "name": "backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b-container",
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
        
    )
        
    

    # Export pod names
    
        
    pulumi.export("backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e_0_name", backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e_0.metadata["name"])
        
    pulumi.export("backend__45a18026_1ab4_4e40_879d_a2c613be709c_1_name", backend__45a18026_1ab4_4e40_879d_a2c613be709c_1.metadata["name"])
        
    pulumi.export("backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b_0_name", backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b_0.metadata["name"])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name="increase-f7f4ec0e-e999-46cd-8fa2-a5d42fbf7e27",
        project_name="pulumi-k8s-./deployment-increase-f7f4ec0e-e999-46cd-8fa2-a5d42fbf7e27",
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

    
        
    print(f"Pod backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e-0 Name: {up_res.outputs['backend_fb80decd_273e_452b_b4a6_328dcb1d4c0e_0_name'].value}")
        
    print(f"Pod backend__45a18026_1ab4_4e40_879d_a2c613be709c-1 Name: {up_res.outputs['backend__45a18026_1ab4_4e40_879d_a2c613be709c_1_name'].value}")
        
    print(f"Pod backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b-0 Name: {up_res.outputs['backend_bc49c9f7_2e0d_407b_ada9_4c5aa2035f3b_0_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name="increase-f7f4ec0e-e999-46cd-8fa2-a5d42fbf7e27",
        project_name="pulumi-k8s-./deployment-increase-f7f4ec0e-e999-46cd-8fa2-a5d42fbf7e27",
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