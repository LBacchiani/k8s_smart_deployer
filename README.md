# k8s_smart_deployer


Before running the tool you need to run Zephyrus2 using the following command:

```
sudo docker pull jacopomauro/zephyrus2
sudo docker run -d -p <PORT>:9001 --name zephyrus_container jacopomauro/zephyrus2
```
where ```<PORT>``` is a user-defined port

To run the tool open a terminal in the root folder and execute 
```
python main.py ARG1 ARG2 ARG3 ARG4 ARG5
```
where

```
ARG1 is the kubelet reserved ram
ARG2 is the kubelet reserved CPU
ARG3 is the path to the components specification
ARG4 is the VMs specification file name (it needs to be in the same path specified as ARG3)
ARG5 is the value of the <PORT> specified after launching the zephyrus2 container
```
