import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775 = k8s.core.v1.Pod("proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775",
        metadata={
            "name": f"proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775",
        },
        spec={
            "containers": [
                {
                    "name": "proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775-container",
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
        
    proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da = k8s.core.v1.Pod("proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da",
        metadata={
            "name": f"proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da",
        },
        spec={
            "containers": [
                {
                    "name": "proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da-container",
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
        
    backend__2e72bab8_8cd4_4070_9b04_c3350c67df87 = k8s.core.v1.Pod("backend__2e72bab8_8cd4_4070_9b04_c3350c67df87",
        metadata={
            "name": f"backend__2e72bab8_8cd4_4070_9b04_c3350c67df87",
        },
        spec={
            "containers": [
                {
                    "name": "backend__2e72bab8_8cd4_4070_9b04_c3350c67df87-container",
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
            
                ['proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775', 'proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da'],
            
        ])
        
    )
        
    backend__0ec20402_bf1a_448c_a073_83e6c7a041b2 = k8s.core.v1.Pod("backend__0ec20402_bf1a_448c_a073_83e6c7a041b2",
        metadata={
            "name": f"backend__0ec20402_bf1a_448c_a073_83e6c7a041b2",
        },
        spec={
            "containers": [
                {
                    "name": "backend__0ec20402_bf1a_448c_a073_83e6c7a041b2-container",
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
            
                ['proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775', 'proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da'],
            
        ])
        
    )
        
    backend_acb32322_f82b_40a7_b8cf_22cddfd71eec = k8s.core.v1.Pod("backend_acb32322_f82b_40a7_b8cf_22cddfd71eec",
        metadata={
            "name": f"backend_acb32322_f82b_40a7_b8cf_22cddfd71eec",
        },
        spec={
            "containers": [
                {
                    "name": "backend_acb32322_f82b_40a7_b8cf_22cddfd71eec-container",
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
            
                ['proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775', 'proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da'],
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export("proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775_name", proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775.metadata["name"])
        
    pulumi.export("proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da_name", proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da.metadata["name"])
        
    pulumi.export("backend__2e72bab8_8cd4_4070_9b04_c3350c67df87_name", backend__2e72bab8_8cd4_4070_9b04_c3350c67df87.metadata["name"])
        
    pulumi.export("backend__0ec20402_bf1a_448c_a073_83e6c7a041b2_name", backend__0ec20402_bf1a_448c_a073_83e6c7a041b2.metadata["name"])
        
    pulumi.export("backend_acb32322_f82b_40a7_b8cf_22cddfd71eec_name", backend_acb32322_f82b_40a7_b8cf_22cddfd71eec.metadata["name"])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name="increase-0ddd4ee7-c300-4079-9260-9f93716a092c",
        project_name="pulumi-k8s-./deployment-increase-0ddd4ee7-c300-4079-9260-9f93716a092c",
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

    
        
    print(f"Pod proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775 Name: {up_res.outputs['proxy__3d6bbef5_8acb_4f42_8eb5_1fe6a56d0775_name'].value}")
        
    print(f"Pod proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da Name: {up_res.outputs['proxy__78bcc39a_28a6_4c73_a4ec_693d766d14da_name'].value}")
        
    print(f"Pod backend__2e72bab8_8cd4_4070_9b04_c3350c67df87 Name: {up_res.outputs['backend__2e72bab8_8cd4_4070_9b04_c3350c67df87_name'].value}")
        
    print(f"Pod backend__0ec20402_bf1a_448c_a073_83e6c7a041b2 Name: {up_res.outputs['backend__0ec20402_bf1a_448c_a073_83e6c7a041b2_name'].value}")
        
    print(f"Pod backend_acb32322_f82b_40a7_b8cf_22cddfd71eec Name: {up_res.outputs['backend_acb32322_f82b_40a7_b8cf_22cddfd71eec_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name="increase-0ddd4ee7-c300-4079-9260-9f93716a092c",
        project_name="pulumi-k8s-./deployment-increase-0ddd4ee7-c300-4079-9260-9f93716a092c",
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