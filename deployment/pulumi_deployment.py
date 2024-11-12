import pulumi
import pulumi_kubernetes as k8s
import os
from pulumi import automation as auto

def pulumi_program():
    
        
    proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea = k8s.core.v1.Pod('proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea',
        metadata=k8s.meta.v1.ObjectMetaArgs(

                name = 'proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea',
                labels = {'app': 'proxy'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea-container',
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
        
    proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344 = k8s.core.v1.Pod('proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344',
                labels = {'app': 'proxy'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344-container',
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
        
    backend__1046dbf1_59e8_4c91_8d65_faa264dd2493 = k8s.core.v1.Pod('backend__1046dbf1_59e8_4c91_8d65_faa264dd2493',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'backend__1046dbf1_59e8_4c91_8d65_faa264dd2493',
                labels = {'app': 'backend'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'backend__1046dbf1_59e8_4c91_8d65_faa264dd2493-container',
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
            
                ['proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea'],
            
        ])
        
    )
        
    backend__48537c5f_ec5b_410c_8dba_80e59d44efee = k8s.core.v1.Pod('backend__48537c5f_ec5b_410c_8dba_80e59d44efee',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'backend__48537c5f_ec5b_410c_8dba_80e59d44efee',
                labels = {'app': 'backend'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'backend__48537c5f_ec5b_410c_8dba_80e59d44efee-container',
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
            
                ['proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea'],
            
        ])
        
    )
        
    backend__532be676_938c_40e1_91cb_69e9dcf7192b = k8s.core.v1.Pod('backend__532be676_938c_40e1_91cb_69e9dcf7192b',
        metadata=k8s.meta.v1.ObjectMetaArgs(
            
                name = 'backend__532be676_938c_40e1_91cb_69e9dcf7192b',
                labels = {'app': 'backend'}
            
        ),
        spec=k8s.core.v1.PodSpecArgs(
            containers = [
                k8s.core.v1.ContainerArgs(
                    name = 'backend__532be676_938c_40e1_91cb_69e9dcf7192b-container',
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
            
                ['proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea'],
            
        ])
        
    )
        
    

    # Export pod names
    
        
    pulumi.export('proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea_name', proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea.metadata['name'])
        
    pulumi.export('proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344_name', proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344.metadata['name'])
        
    pulumi.export('backend__1046dbf1_59e8_4c91_8d65_faa264dd2493_name', backend__1046dbf1_59e8_4c91_8d65_faa264dd2493.metadata['name'])
        
    pulumi.export('backend__48537c5f_ec5b_410c_8dba_80e59d44efee_name', backend__48537c5f_ec5b_410c_8dba_80e59d44efee.metadata['name'])
        
    pulumi.export('backend__532be676_938c_40e1_91cb_69e9dcf7192b_name', backend__532be676_938c_40e1_91cb_69e9dcf7192b.metadata['name'])
        
    

def deploy_orchestration():
    stack = auto.create_or_select_stack(
        stack_name='increase-a78966c7-2e7a-46ec-b951-9cc9d6ad4507',
        project_name='pulumi-k8s-increase-a78966c7-2e7a-46ec-b951-9cc9d6ad4507',
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

    
        
    print(f"Pod proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea Name: {up_res.outputs['proxy__68ef77e3_a4b0_43a9_8bf8_cd4b3f65bfea_name'].value}")
        
    print(f"Pod proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344 Name: {up_res.outputs['proxy_ed3b4fd9_bcb9_4843_bd37_de123c0ba344_name'].value}")
        
    print(f"Pod backend__1046dbf1_59e8_4c91_8d65_faa264dd2493 Name: {up_res.outputs['backend__1046dbf1_59e8_4c91_8d65_faa264dd2493_name'].value}")
        
    print(f"Pod backend__48537c5f_ec5b_410c_8dba_80e59d44efee Name: {up_res.outputs['backend__48537c5f_ec5b_410c_8dba_80e59d44efee_name'].value}")
        
    print(f"Pod backend__532be676_938c_40e1_91cb_69e9dcf7192b Name: {up_res.outputs['backend__532be676_938c_40e1_91cb_69e9dcf7192b_name'].value}")
        
    

def destroy_pods():
    stack = auto.create_or_select_stack(
        stack_name='increase-a78966c7-2e7a-46ec-b951-9cc9d6ad4507',
        project_name='pulumi-k8s-increase-a78966c7-2e7a-46ec-b951-9cc9d6ad4507',
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