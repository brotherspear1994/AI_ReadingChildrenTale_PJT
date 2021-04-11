ARG CUDA="9.0"
ARG CUDNN="7"

FROM nvidia/cuda:${CUDA}-cudnn${CUDNN}-devel-ubuntu16.04
CMD nvidia-smi
RUN NVIDIA_VISIBLE_DEVICES=2
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

#RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
#RUN curl -LO https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
#RUN curl -LO https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list

#RUN apt-get update && apt-get install -y nvidia-container-toolkit
#RUN systemctl restart docker

# install basics
RUN apt-get update -y \
 && apt-get install -y apt-utils git curl ca-certificates bzip2 cmake tree htop bmon iotop g++ \
 && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev

# Install Miniconda
RUN curl -LO https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
 && bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b \
 && rm Miniconda3-latest-Linux-x86_64.sh
RUN ls 
ENV PATH=/miniconda/bin:$PATH

# Create a Python 3.6 environment
RUN /miniconda/bin/conda install -y conda-build \
 && /miniconda/bin/conda create -y --name py36 python=3.6.8 \
 && /miniconda/bin/conda clean -ya

RUN pip install --upgrade pip

ENV CONDA_DEFAULT_ENV=py36
ENV CONDA_PREFIX=/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

RUN conda install -y ipython
RUN pip install requests ninja yacs cython matplotlib opencv-python tqdm

# Install PyTorch 1.0 Nightly
ARG CUDA
RUN conda install pytorch==1.4 torchvision==0.5.0 cudatoolkit=${CUDA} -c pytorch \
 && conda clean -ya

# Install TorchVision master

#RUN git clone https://github.com/pytorch/vision.git \
# && cd vision \
# && python setup.py install

# install pycocotools
#RUN git clone https://github.com/cocodataset/cocoapi.git \
# && cd cocoapi/PythonAPI \
# && python setup.py build_ext install

# install apex
#RUN git clone https://github.com/NVIDIA/apex.git \
# && cd apex \
# && python setup.py install --cuda_ext --cpp_ext

# install PyTorch Detection
ARG FORCE_CUDA="1"
ENV FORCE_CUDA=${FORCE_CUDA}
RUN git clone https://github.com/facebookresearch/maskrcnn-benchmark.git \
 && cd maskrcnn-benchmark \
 && python setup.py build develop

WORKDIR /maskrcnn-benchmark
