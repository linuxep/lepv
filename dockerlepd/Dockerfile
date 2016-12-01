FROM ubuntu:14.04

RUN apt-get update
#RUN apt-get install libev-dev linux-tools-common linux-tools-generic

RUN apt-get install -y libev-dev
RUN apt-get install -y linux-tools-common
RUN apt-get install -y linux-tools-generic

WORKDIR /opt
RUN apt-get install -y git
RUN git clone https://github.com/linuxep/lepd.git

# Run LEPD with root permission
USER root

WORKDIR /opt/lepd/prebuilt-binaries
ENTRYPOINT ["sudo", "./x86-lepd", "&"]