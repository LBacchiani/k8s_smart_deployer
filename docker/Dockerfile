FROM python:latest

RUN apt-get update && \
    pip install \
    pyyaml \
    bidict

COPY --from=jacopomauro/zephyrus2:latest /tool/ /tool/

# clone k8s_smart_deployer
RUN cd /tool && \
    git clone https://github.com/LBacchiani/k8s_smart_deployer.git

ENV PATH /tool/k8s_smart_deployer:$PATH

WORKDIR /tool/k8s_smart_deployer
CMD ["/bin/bash"]