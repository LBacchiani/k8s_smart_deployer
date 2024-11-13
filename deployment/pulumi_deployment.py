import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0 = k8s.core.v1.Pod('proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0',
                labels = {'app': 'proxy'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0-container',
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
        
    proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2 = k8s.core.v1.Pod('proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2',
                labels = {'app': 'proxy'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2-container',
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
        
    backend__04b6099d_d886_4f0e_a7e1_472f86f27d31 = k8s.core.v1.Pod('backend__04b6099d_d886_4f0e_a7e1_472f86f27d31',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'backend__04b6099d_d886_4f0e_a7e1_472f86f27d31',
                labels = {'app': 'backend'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'backend__04b6099d_d886_4f0e_a7e1_472f86f27d31-container',
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
            
                ['proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0'],
            
        ])
        
    )
        
    backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d = k8s.core.v1.Pod('backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d',
                labels = {'app': 'backend'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d-container',
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
            
                ['proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0'],
            
        ])
        
    )
        
    backend__1591808d_720a_4e97_9e48_b04db43a0677 = k8s.core.v1.Pod('backend__1591808d_720a_4e97_9e48_b04db43a0677',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'backend__1591808d_720a_4e97_9e48_b04db43a0677',
                labels = {'app': 'backend'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'backend__1591808d_720a_4e97_9e48_b04db43a0677-container',
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
            
                ['proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0'],
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export('proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0_name', proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0.metadata['name'])
        
    pulumi.export('proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2_name', proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2.metadata['name'])
        
    pulumi.export('backend__04b6099d_d886_4f0e_a7e1_472f86f27d31_name', backend__04b6099d_d886_4f0e_a7e1_472f86f27d31.metadata['name'])
        
    pulumi.export('backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d_name', backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d.metadata['name'])
        
    pulumi.export('backend__1591808d_720a_4e97_9e48_b04db43a0677_name', backend__1591808d_720a_4e97_9e48_b04db43a0677.metadata['name'])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name='increase-c158221f-8b9b-4351-a5ed-76d110ae38f5',
        project_name='pulumi-k8s-increase-c158221f-8b9b-4351-a5ed-76d110ae38f5',
        program=pulumi_program
    )

    print('Successfully initialized stack')

    kubeconfig_path = os.getenv('KUBECONFIG', '~/.kube/config')
    print(f"Using kubeconfig: {kubeconfig_path}")

    print('Refreshing stack...')
    stack.refresh(on_output=print)

    print('Previewing changes...')
    stack.preview(on_output=print)

    print('Deploying changes...')
    up_res = stack.up(on_output=print)

    
        
    print(f"Pod proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0 Name: {up_res.outputs['proxy__3a7407f9_f00a_4880_9a26_4c70b9256aa0_name'].value}")
        
    print(f"Pod proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2 Name: {up_res.outputs['proxy__2db8bf88_492a_4bf7_ad7a_6caa3398abd2_name'].value}")
        
    print(f"Pod backend__04b6099d_d886_4f0e_a7e1_472f86f27d31 Name: {up_res.outputs['backend__04b6099d_d886_4f0e_a7e1_472f86f27d31_name'].value}")
        
    print(f"Pod backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d Name: {up_res.outputs['backend__18bc56a3_243b_4fe9_a925_3cc8ee5eeb0d_name'].value}")
        
    print(f"Pod backend__1591808d_720a_4e97_9e48_b04db43a0677 Name: {up_res.outputs['backend__1591808d_720a_4e97_9e48_b04db43a0677_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name='increase-c158221f-8b9b-4351-a5ed-76d110ae38f5',
        project_name='pulumi-k8s-increase-c158221f-8b9b-4351-a5ed-76d110ae38f5',
        program=lambda: None
    )

    print('Destroying resources...')
    stack.destroy(on_output=print)
    print('Resources successfully destroyed.')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'destroy':
       destroy_pods()
    else:
        deploy_orchestration()