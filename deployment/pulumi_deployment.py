import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    proxy_a26e3655_d2f7_464d_b561_02022707805f = k8s.core.v1.Pod("proxy_a26e3655_d2f7_464d_b561_02022707805f",
        metadata={
            "name": f"proxy_a26e3655_d2f7_464d_b561_02022707805f",
        },
        spec={
            "containers": [
                {
                    "name": "proxy_a26e3655_d2f7_464d_b561_02022707805f-container",
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
        
    proxy__77ad5997_746a_4787_9bf7_1b20862c2619 = k8s.core.v1.Pod("proxy__77ad5997_746a_4787_9bf7_1b20862c2619",
        metadata={
            "name": f"proxy__77ad5997_746a_4787_9bf7_1b20862c2619",
        },
        spec={
            "containers": [
                {
                    "name": "proxy__77ad5997_746a_4787_9bf7_1b20862c2619-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "450m",
                            "memory": "600M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-1"
        }
        
    )
        
    backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86 = k8s.core.v1.Pod("backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86",
        metadata={
            "name": f"backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86",
        },
        spec={
            "containers": [
                {
                    "name": "backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-2"
        }
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                ['proxy_a26e3655_d2f7_464d_b561_02022707805f', 'proxy__77ad5997_746a_4787_9bf7_1b20862c2619'],
            
        ])
        
    )
        
    backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0 = k8s.core.v1.Pod("backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0",
        metadata={
            "name": f"backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0",
        },
        spec={
            "containers": [
                {
                    "name": "backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0-container",
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
            
                ['proxy_a26e3655_d2f7_464d_b561_02022707805f', 'proxy__77ad5997_746a_4787_9bf7_1b20862c2619'],
            
        ])
        
    )
        
    backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c = k8s.core.v1.Pod("backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c",
        metadata={
            "name": f"backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c",
        },
        spec={
            "containers": [
                {
                    "name": "backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c-container",
                    "image": "k8s.gcr.io/pause:2.0",
                    "resources": {
                        "requests": {
                            "cpu": "300m",
                            "memory": "500M"
                        }
                    }
                }
            ],
            "nodeName": "k3d-k3s-default-agent-2"
        }
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                ['proxy_a26e3655_d2f7_464d_b561_02022707805f', 'proxy__77ad5997_746a_4787_9bf7_1b20862c2619'],
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export("proxy_a26e3655_d2f7_464d_b561_02022707805f_name", proxy_a26e3655_d2f7_464d_b561_02022707805f.metadata["name"])
        
    pulumi.export("proxy__77ad5997_746a_4787_9bf7_1b20862c2619_name", proxy__77ad5997_746a_4787_9bf7_1b20862c2619.metadata["name"])
        
    pulumi.export("backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86_name", backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86.metadata["name"])
        
    pulumi.export("backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0_name", backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0.metadata["name"])
        
    pulumi.export("backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c_name", backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c.metadata["name"])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name="increase-241281c2-dd30-413c-8be5-78c1844d2353",
        project_name="pulumi-k8s-./deployment-increase-241281c2-dd30-413c-8be5-78c1844d2353",
        program=pulumi_program
    )

    print("Successfully initialized stack")

    kubeconfig_path = os.getenv('KUBECONFIG', '~/.kube/config')
    print(f"Using kubeconfig: {kubeconfig_path}")

    print("Refreshing stack...")
    stack.refresh(on_output=print)

    print("Previewing changes...")
    stack.preview(on_output=print)

    print("Deploying changes...")
    up_res = stack.up(on_output=print)

    
        
    print(f"Pod proxy_a26e3655_d2f7_464d_b561_02022707805f Name: {up_res.outputs['proxy_a26e3655_d2f7_464d_b561_02022707805f_name'].value}")
        
    print(f"Pod proxy__77ad5997_746a_4787_9bf7_1b20862c2619 Name: {up_res.outputs['proxy__77ad5997_746a_4787_9bf7_1b20862c2619_name'].value}")
        
    print(f"Pod backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86 Name: {up_res.outputs['backend__5a208d0f_3ab6_4493_be1d_6b433e24eb86_name'].value}")
        
    print(f"Pod backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0 Name: {up_res.outputs['backend_deb6a4be_6570_40e6_ad5b_d527c48c47c0_name'].value}")
        
    print(f"Pod backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c Name: {up_res.outputs['backend__754fa0e1_36ae_42a6_b861_8e405dc4ff1c_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name="increase-241281c2-dd30-413c-8be5-78c1844d2353",
        project_name="pulumi-k8s-./deployment-increase-241281c2-dd30-413c-8be5-78c1844d2353",
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