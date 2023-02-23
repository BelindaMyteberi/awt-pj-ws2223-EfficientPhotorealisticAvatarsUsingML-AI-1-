FROM python:3.9-slim
WORKDIR /neural-heads
COPY setup.py ./
COPY ./neural-head-avatars ./
RUN apt-get update && apt-get install -y git wget software-properties-common
RUN wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-debian11-11-7-local_11.7.0-515.43.04-1_amd64.deb
RUN dpkg -i cuda-repo-debian11-11-7-local_11.7.0-515.43.04-1_amd64.deb
RUN cp /var/cuda-repo-debian11-11-7-local/cuda-*-keyring.gpg /usr/share/keyrings/
RUN add-apt-repository contrib
RUN apt-get update
RUN apt-get -y install cuda-11-7
RUN python -m pip install --upgrade pip
RUN pip install torch==1.12.0+cu113 torchvision==0.13.0+cu113 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install "git+https://github.com/facebookresearch/pytorch3d.git@stable"
RUN pip install -e .
# Copy the rest of the application code to the container
#WORKDIR /neural-heads/python_scripts
#Installation
RUN pip install -e deps/video-head-tracker
# #Head Tracking
# RUN python /neural-heads/deps/video-head-tracker/vht/optimize_tracking.py --config /neural-heads/configs/tracking.ini
# #Avatar Optimization 
# RUN python /neural-heads/python_scripts/optimize_nha.py --config /neural-heads/configs/optimize_avatar.ini
# #Reenacting an optimized Avatar:
# RUN python /neural-heads/python_scripts/reenact_avatar.py --config /neural-heads/configs/reenactment.ini
# CMD ["python", "/neural-heads/python_scripts/video_to_dataset.py","--video", "/neural-heads/input/", "--out_path", "/neural-heads/output/"]
# VOLUME /app/output/