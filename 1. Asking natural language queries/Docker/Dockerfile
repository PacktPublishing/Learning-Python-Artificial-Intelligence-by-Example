FROM ubuntu:16.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget
RUN apt-get install -y bzip2

# Setup locale
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

# Install Anaconda
RUN wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
RUN bash /Anaconda3-5.1.0-Linux-x86_64.sh -b \
    && echo "export PATH='$HOME/anaconda3/bin:$PATH'" >> ~/.bashrc
ENV PATH="${PATH}:/root/anaconda3/bin"

# Setup Python environment
RUN conda update -n base conda
RUN pip install --upgrade pip
RUN pip install wptools
RUN pip install gensim
RUN pip install nltk
RUN pip install flask
RUN pip install flask_restful









