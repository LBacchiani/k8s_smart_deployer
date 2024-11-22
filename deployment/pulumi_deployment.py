import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto
import uuid

def create_pod_name(service_name, stack_name):
    """Generate a unique pod name based on service and stack"""
    return f"{service_name}-{stack_name}"

def pulumi_program():
    stack = pulumi.get_stack()

    
        
    proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279_name = create_pod_name('proxy-8a2d9e2c-6216-49a6-b199-3c800acc5279', stack)

    proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279 = k8s.core.v1.Pod(proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279_name,
                labels = {
                    **{'app': 'proxy'},
                    'stack': stack,
                    'original_service': 'proxy-8a2d9e2c-6216-49a6-b199-3c800acc5279'
                }
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'k8s-gcr-io-pause-2-0',
                    image = 'k8s.gcr.io/pause:2.0',
                    resources=k8s.core.v1.ResourceRequirementsArgs(
                        requests= {
                            'cpu': '450m',
                            'memory': '600M'
                        }
                    )
                )
            ],
            node_name = 'k3d-k3s-default-agent-1'
        )
        
    )
        
    proxy_16158165_fded_4ba6_971b_5737e02fa856_name = create_pod_name('proxy-16158165-fded-4ba6-971b-5737e02fa856', stack)

    proxy_16158165_fded_4ba6_971b_5737e02fa856 = k8s.core.v1.Pod(proxy_16158165_fded_4ba6_971b_5737e02fa856_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = proxy_16158165_fded_4ba6_971b_5737e02fa856_name,
                labels = {
                    **{'app': 'proxy'},
                    'stack': stack,
                    'original_service': 'proxy-16158165-fded-4ba6-971b-5737e02fa856'
                }
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'k8s-gcr-io-pause-2-0',
                    image = 'k8s.gcr.io/pause:2.0',
                    resources=k8s.core.v1.ResourceRequirementsArgs(
                        requests= {
                            'cpu': '450m',
                            'memory': '600M'
                        }
                    )
                )
            ],
            node_name = 'k3d-k3s-default-agent-0'
        )
        
    )
        
    backend_1601219e_bf6a_41e3_bfe6_7f5a2ca1fc5d_name = create_pod_name('backend-1601219e-bf6a-41e3-bfe6-7f5a2ca1fc5d', stack)

    backend_1601219e_bf6a_41e3_bfe6_7f5a2ca1fc5d = k8s.core.v1.Pod(backend_1601219e_bf6a_41e3_bfe6_7f5a2ca1fc5d_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = backend_1601219e_bf6a_41e3_bfe6_7f5a2ca1fc5d_name,
                labels = {
                    **{'app': 'backend'},
                    'stack': stack,
                    'original_service': 'backend-1601219e-bf6a-41e3-bfe6-7f5a2ca1fc5d'
                }
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'k8s-gcr-io-pause-2-0',
                    image = 'k8s.gcr.io/pause:2.0',
                    resources=k8s.core.v1.ResourceRequirementsArgs(
                        requests= {
                            'cpu': '300m',
                            'memory': '500M'
                        }
                    )
                )
            ],
            node_name = 'k3d-k3s-default-agent-2'
        )
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                
                    proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279,
                
            
        ])
        
    )
        
    backend_bb93b78a_3cca_4a03_9724_bdd7b1352639_name = create_pod_name('backend-bb93b78a-3cca-4a03-9724-bdd7b1352639', stack)

    backend_bb93b78a_3cca_4a03_9724_bdd7b1352639 = k8s.core.v1.Pod(backend_bb93b78a_3cca_4a03_9724_bdd7b1352639_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = backend_bb93b78a_3cca_4a03_9724_bdd7b1352639_name,
                labels = {
                    **{'app': 'backend'},
                    'stack': stack,
                    'original_service': 'backend-bb93b78a-3cca-4a03-9724-bdd7b1352639'
                }
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'k8s-gcr-io-pause-2-0',
                    image = 'k8s.gcr.io/pause:2.0',
                    resources=k8s.core.v1.ResourceRequirementsArgs(
                        requests= {
                            'cpu': '300m',
                            'memory': '500M'
                        }
                    )
                )
            ],
            node_name = 'k3d-k3s-default-agent-2'
        )
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                
                    proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279,
                
            
        ])
        
    )
        
    backend_bdee159f_c3df_4086_bfeb_419078b18847_name = create_pod_name('backend-bdee159f-c3df-4086-bfeb-419078b18847', stack)

    backend_bdee159f_c3df_4086_bfeb_419078b18847 = k8s.core.v1.Pod(backend_bdee159f_c3df_4086_bfeb_419078b18847_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = backend_bdee159f_c3df_4086_bfeb_419078b18847_name,
                labels = {
                    **{'app': 'backend'},
                    'stack': stack,
                    'original_service': 'backend-bdee159f-c3df-4086-bfeb-419078b18847'
                }
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'k8s-gcr-io-pause-2-0',
                    image = 'k8s.gcr.io/pause:2.0',
                    resources=k8s.core.v1.ResourceRequirementsArgs(
                        requests= {
                            'cpu': '300m',
                            'memory': '500M'
                        }
                    )
                )
            ],
            node_name = 'k3d-k3s-default-agent-1'
        )
        
        ,opts=pulumi.ResourceOptions(depends_on=[
            
                
                    proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279,
                
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export('proxy-8a2d9e2c-6216-49a6-b199-3c800acc5279_name', proxy_8a2d9e2c_6216_49a6_b199_3c800acc5279.metadata['name'])
        
    pulumi.export('proxy-16158165-fded-4ba6-971b-5737e02fa856_name', proxy_16158165_fded_4ba6_971b_5737e02fa856.metadata['name'])
        
    pulumi.export('backend-1601219e-bf6a-41e3-bfe6-7f5a2ca1fc5d_name', backend_1601219e_bf6a_41e3_bfe6_7f5a2ca1fc5d.metadata['name'])
        
    pulumi.export('backend-bb93b78a-3cca-4a03-9724-bdd7b1352639_name', backend_bb93b78a_3cca_4a03_9724_bdd7b1352639.metadata['name'])
        
    pulumi.export('backend-bdee159f-c3df-4086-bfeb-419078b18847_name', backend_bdee159f_c3df_4086_bfeb_419078b18847.metadata['name'])
        
    

def deploy_orchestration(stack_name):
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name='pulumi-k8s-increase-bc1c4864-17b1-4930-80ff-1f2a3ced38eb',
        program=pulumi_program
    )

    print(f'Successfully initialized stack: {stack_name}')

    kubeconfig_path = os.getenv('KUBECONFIG', '~/.kube/config')
    print(f"Using kubeconfig: {kubeconfig_path}")

    print('Refreshing stack...')
    stack.refresh(on_output=print)

    print('Previewing changes...')
    stack.preview(on_output=print)

    print('Deploying changes...')
    up_res = stack.up(on_output=print)

    print(f"\nPods created in stack '{stack_name}':")
    
        
    print(f"Pod proxy-8a2d9e2c-6216-49a6-b199-3c800acc5279 Name: {up_res.outputs['proxy-8a2d9e2c-6216-49a6-b199-3c800acc5279_name'].value}")
        
    print(f"Pod proxy-16158165-fded-4ba6-971b-5737e02fa856 Name: {up_res.outputs['proxy-16158165-fded-4ba6-971b-5737e02fa856_name'].value}")
        
    print(f"Pod backend-1601219e-bf6a-41e3-bfe6-7f5a2ca1fc5d Name: {up_res.outputs['backend-1601219e-bf6a-41e3-bfe6-7f5a2ca1fc5d_name'].value}")
        
    print(f"Pod backend-bb93b78a-3cca-4a03-9724-bdd7b1352639 Name: {up_res.outputs['backend-bb93b78a-3cca-4a03-9724-bdd7b1352639_name'].value}")
        
    print(f"Pod backend-bdee159f-c3df-4086-bfeb-419078b18847 Name: {up_res.outputs['backend-bdee159f-c3df-4086-bfeb-419078b18847_name'].value}")
        
    

def destroy_pods(stack_name):
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name='pulumi-k8s-increase-bc1c4864-17b1-4930-80ff-1f2a3ced38eb',
        program=lambda: None
    )

    print(f'Destroying resources in stack: {stack_name}...')
    stack.destroy(on_output=print)
    print('Resources successfully destroyed.')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py stack_name [destroy]")
        sys.exit(1)

    stack_name = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == 'destroy':
        destroy_pods(stack_name)
    else:
        deploy_orchestration(stack_name)