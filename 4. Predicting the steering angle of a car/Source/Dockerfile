FROM tensorflow/tensorflow:latest-py3
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget
RUN apt-get install -y bzip2

# Setup locale
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

# Install other dependencies
RUN apt install -y python-opencv
RUN pip install pandas
RUN pip install keras
RUN apt-get install -y graphviz
RUN pip install pydot

