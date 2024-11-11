# k8s_smart_deployer


Before running the tool you need to run Zephyrus2 using the following command:

```
sudo docker pull jacopomauro/zephyrus2
sudo docker run -d -p <PORT>:9001 --name zephyrus_container jacopomauro/zephyrus2
```
where ```<PORT>``` is a user-defined port

To run the tool open a terminal in the root folder and execute 
```
python main.py ARG1 ARG2 ARG3
```
where

```
ARG1 is the path to the declarative specifications of services and resources
ARG2 is the value of the <PORT> specified after launching the zephyrus2 container
ARG3 is the orchestration language
```

Currently, we only support ```YAML``` and ```Python``` as orchestration languages. To choose among them, 
use ```yaml``` and ```py```
