import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    proxy__119aa883_e154_40ca_91ce_26ae816ed44c = k8s.core.v1.Pod("proxy__119aa883_e154_40ca_91ce_26ae816ed44c",
        metadata={
            "name": f"proxy__119aa883_e154_40ca_91ce_26ae816ed44c",
        },
        spec={
            "containers": [
                {
                    "name": "proxy__119aa883_e154_40ca_91ce_26ae816ed44c-container",
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
        
    proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5 = k8s.core.v1.Pod("proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5",
        metadata={
            "name": f"proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5",
        },
        spec={
            "containers": [
                {
                    "name": "proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5-container",
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
        
    backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631 = k8s.core.v1.Pod("backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631",
        metadata={
            "name": f"backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631",
        },
        spec={
            "containers": [
                {
                    "name": "backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631-container",
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
            
                ['proxy__119aa883_e154_40ca_91ce_26ae816ed44c'],
            
        ])
        
    )
        
    backend__915cd032_b4fe_4453_9a72_84543a599ab0 = k8s.core.v1.Pod("backend__915cd032_b4fe_4453_9a72_84543a599ab0",
        metadata={
            "name": f"backend__915cd032_b4fe_4453_9a72_84543a599ab0",
        },
        spec={
            "containers": [
                {
                    "name": "backend__915cd032_b4fe_4453_9a72_84543a599ab0-container",
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
            
                ['proxy__119aa883_e154_40ca_91ce_26ae816ed44c'],
            
        ])
        
    )
        
    backend__822426e6_7048_4a4f_9006_7a4af372d5da = k8s.core.v1.Pod("backend__822426e6_7048_4a4f_9006_7a4af372d5da",
        metadata={
            "name": f"backend__822426e6_7048_4a4f_9006_7a4af372d5da",
        },
        spec={
            "containers": [
                {
                    "name": "backend__822426e6_7048_4a4f_9006_7a4af372d5da-container",
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
            
                ['proxy__119aa883_e154_40ca_91ce_26ae816ed44c'],
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export("proxy__119aa883_e154_40ca_91ce_26ae816ed44c_name", proxy__119aa883_e154_40ca_91ce_26ae816ed44c.metadata["name"])
        
    pulumi.export("proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5_name", proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5.metadata["name"])
        
    pulumi.export("backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631_name", backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631.metadata["name"])
        
    pulumi.export("backend__915cd032_b4fe_4453_9a72_84543a599ab0_name", backend__915cd032_b4fe_4453_9a72_84543a599ab0.metadata["name"])
        
    pulumi.export("backend__822426e6_7048_4a4f_9006_7a4af372d5da_name", backend__822426e6_7048_4a4f_9006_7a4af372d5da.metadata["name"])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name="increase-140c19f6-d502-4405-9b31-60212600d032",
        project_name="pulumi-k8s-./deployment-increase-140c19f6-d502-4405-9b31-60212600d032",
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

    
        
    print(f"Pod proxy__119aa883_e154_40ca_91ce_26ae816ed44c Name: {up_res.outputs['proxy__119aa883_e154_40ca_91ce_26ae816ed44c_name'].value}")
        
    print(f"Pod proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5 Name: {up_res.outputs['proxy__89e7ce31_f9bc_4451_8b50_3b9d29bfd2b5_name'].value}")
        
    print(f"Pod backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631 Name: {up_res.outputs['backend_cf3f22af_4fb0_4beb_9c34_6f04fcd35631_name'].value}")
        
    print(f"Pod backend__915cd032_b4fe_4453_9a72_84543a599ab0 Name: {up_res.outputs['backend__915cd032_b4fe_4453_9a72_84543a599ab0_name'].value}")
        
    print(f"Pod backend__822426e6_7048_4a4f_9006_7a4af372d5da Name: {up_res.outputs['backend__822426e6_7048_4a4f_9006_7a4af372d5da_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name="increase-140c19f6-d502-4405-9b31-60212600d032",
        project_name="pulumi-k8s-./deployment-increase-140c19f6-d502-4405-9b31-60212600d032",
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