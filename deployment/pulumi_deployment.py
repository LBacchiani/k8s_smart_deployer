import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto
import uuid

def create_pod_name(service_name, stack_name):
    """Generate a unique pod name based on service and stack"""
    return f"{service_name}-{stack_name}-{str(uuid.uuid4())[:8]}"

def pulumi_program():
    stack = pulumi.get_stack()

    
        
    proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9_name = create_pod_name('proxy-ae23c5a1-39fb-4bfd-8d30-940d94272cb9', stack)

    proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9 = k8s.core.v1.Pod(proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9_name,
                labels = {
                    **{'app': 'proxy'},
                    'stack': stack,
                    'original_service': 'proxy-ae23c5a1-39fb-4bfd-8d30-940d94272cb9'
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
        
    proxy_2e42ec34_9267_4e56_9f6c_47eca3f98440_name = create_pod_name('proxy-2e42ec34-9267-4e56-9f6c-47eca3f98440', stack)

    proxy_2e42ec34_9267_4e56_9f6c_47eca3f98440 = k8s.core.v1.Pod(proxy_2e42ec34_9267_4e56_9f6c_47eca3f98440_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = proxy_2e42ec34_9267_4e56_9f6c_47eca3f98440_name,
                labels = {
                    **{'app': 'proxy'},
                    'stack': stack,
                    'original_service': 'proxy-2e42ec34-9267-4e56-9f6c-47eca3f98440'
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
        
    backend_557195d6_5432_4ae9_8ca5_7d7ef07f428c_name = create_pod_name('backend-557195d6-5432-4ae9-8ca5-7d7ef07f428c', stack)

    backend_557195d6_5432_4ae9_8ca5_7d7ef07f428c = k8s.core.v1.Pod(backend_557195d6_5432_4ae9_8ca5_7d7ef07f428c_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = backend_557195d6_5432_4ae9_8ca5_7d7ef07f428c_name,
                labels = {
                    **{'app': 'backend'},
                    'stack': stack,
                    'original_service': 'backend-557195d6-5432-4ae9-8ca5-7d7ef07f428c'
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
            
                
                    proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9,
                
            
        ])
        
    )
        
    backend_31dc2f08_16f3_4830_8974_81fe10d009ae_name = create_pod_name('backend-31dc2f08-16f3-4830-8974-81fe10d009ae', stack)

    backend_31dc2f08_16f3_4830_8974_81fe10d009ae = k8s.core.v1.Pod(backend_31dc2f08_16f3_4830_8974_81fe10d009ae_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = backend_31dc2f08_16f3_4830_8974_81fe10d009ae_name,
                labels = {
                    **{'app': 'backend'},
                    'stack': stack,
                    'original_service': 'backend-31dc2f08-16f3-4830-8974-81fe10d009ae'
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
            
                
                    proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9,
                
            
        ])
        
    )
        
    backend_f99c6036_9467_4675_9582_c86fb849632a_name = create_pod_name('backend-f99c6036-9467-4675-9582-c86fb849632a', stack)

    backend_f99c6036_9467_4675_9582_c86fb849632a = k8s.core.v1.Pod(backend_f99c6036_9467_4675_9582_c86fb849632a_name,
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = backend_f99c6036_9467_4675_9582_c86fb849632a_name,
                labels = {
                    **{'app': 'backend'},
                    'stack': stack,
                    'original_service': 'backend-f99c6036-9467-4675-9582-c86fb849632a'
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
            
                
                    proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9,
                
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export('proxy-ae23c5a1-39fb-4bfd-8d30-940d94272cb9_name', proxy_ae23c5a1_39fb_4bfd_8d30_940d94272cb9.metadata['name'])
        
    pulumi.export('proxy-2e42ec34-9267-4e56-9f6c-47eca3f98440_name', proxy_2e42ec34_9267_4e56_9f6c_47eca3f98440.metadata['name'])
        
    pulumi.export('backend-557195d6-5432-4ae9-8ca5-7d7ef07f428c_name', backend_557195d6_5432_4ae9_8ca5_7d7ef07f428c.metadata['name'])
        
    pulumi.export('backend-31dc2f08-16f3-4830-8974-81fe10d009ae_name', backend_31dc2f08_16f3_4830_8974_81fe10d009ae.metadata['name'])
        
    pulumi.export('backend-f99c6036-9467-4675-9582-c86fb849632a_name', backend_f99c6036_9467_4675_9582_c86fb849632a.metadata['name'])
        
    

def deploy_orchestration(stack_name):
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name='pulumi-k8s-increase-df55f0dd-5ae8-4238-bfaa-468f9f3ccab7',
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
    
        
    print(f"Pod proxy-ae23c5a1-39fb-4bfd-8d30-940d94272cb9 Name: {up_res.outputs['proxy-ae23c5a1-39fb-4bfd-8d30-940d94272cb9_name'].value}")
        
    print(f"Pod proxy-2e42ec34-9267-4e56-9f6c-47eca3f98440 Name: {up_res.outputs['proxy-2e42ec34-9267-4e56-9f6c-47eca3f98440_name'].value}")
        
    print(f"Pod backend-557195d6-5432-4ae9-8ca5-7d7ef07f428c Name: {up_res.outputs['backend-557195d6-5432-4ae9-8ca5-7d7ef07f428c_name'].value}")
        
    print(f"Pod backend-31dc2f08-16f3-4830-8974-81fe10d009ae Name: {up_res.outputs['backend-31dc2f08-16f3-4830-8974-81fe10d009ae_name'].value}")
        
    print(f"Pod backend-f99c6036-9467-4675-9582-c86fb849632a Name: {up_res.outputs['backend-f99c6036-9467-4675-9582-c86fb849632a_name'].value}")
        
    

def destroy_pods(stack_name):
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name='pulumi-k8s-increase-df55f0dd-5ae8-4238-bfaa-468f9f3ccab7',
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