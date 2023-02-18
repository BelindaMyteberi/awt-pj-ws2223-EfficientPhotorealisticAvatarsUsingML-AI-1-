FROM python:3.9-slim
WORKDIR /neural-heads
COPY setup.py ./
COPY python_scripts/ /neural-heads/python_scripts/
COPY input/ /neural-heads/input/
COPY deps/ /neural-heads/deps/
COPY configs/ /neural-heads/configs/
RUN apt-get update && apt-get install -y git
#RUN pip install torchvision 
#RUN pip install torch-geometric
#RUN pip install pytorch3d
RUN pip install torch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0
RUN pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu116
RUN pip install -e .
# Copy the rest of the application code to the container
#WORKDIR /neural-heads/python_scripts
#Installation
RUN pip install -e deps/video-head-tracker
#Head Tracking
RUN python /neural-heads/deps/video-head-tracker/vht/optimize_tracking.py --config /neural-heads/configs/tracking.ini
#Avatar Optimization 
RUN python /neural-heads/python_scripts/optimize_nha.py --config /neural-heads/configs/optimize_avatar.ini
#Reenacting an optimized Avatar:
RUN python /neural-heads/python_scripts/reenact_avatar.py --config /neural-heads/configs/reenactment.ini
CMD ["python", "/neural-heads/python_scripts/video_to_dataset.py","--video", "/neural-heads/input/", "--out_path", "/neural-heads/output/"]
VOLUME /app/output/