# k8s_smart_deployer


Before running the tool you need to run Zephyrus2 using the following command:

```
sudo docker pull jacopomauro/zephyrus2
sudo docker run -d -p <PORT>:9001 --name zephyrus_container jacopomauro/zephyrus2
```
where ```<PORT>``` is a user-defined port

To run the tool open a terminal in the root folder and execute 
```
python main.py ARG1 ARG2 ARG3 ARG4 ARG5 ARG6
```
where

```
ARG1 is the folder where microservice specifications are
ARG2 is the yaml file containing the target configuration requirements
ARG3 is the yaml file containing virtual machines requirements
ARG4 is the value of the <PORT> specified after launching the zephyrus2 container
ARG5 is the orchestration language (currently, we only support ```YAML``` and ```Python``` as orchestration languages. To choose among them, 
use ```yaml``` and ```python```)
```
Notice that, all paths must be specified without the final "/"


We currently support two kinds of deployment preferences (considered as "hard" constraints, i.e., they must be satisfied during service scheduling): affinity and antiAffinity. 
The former ensures that the operators used within its context are satisfied, while the latter ensures that the negation of the operators used within its context are satisfied.
Concerning operators, we currently support the In operator. When such operator is used in the context of an affinity preference, it ensures that the specified services are deployed within the same node. Conversely, when it is used in the context of an antiAffinity preference it ensures that the specified services are deployed different nodes.
Notice that, this tool is a proof-of-concept, its stable version will comprise all Kuberentes operators.

Examples are provided in annotation_examples
