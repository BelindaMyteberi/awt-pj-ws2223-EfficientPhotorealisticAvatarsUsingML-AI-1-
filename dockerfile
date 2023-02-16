FROM python:3.9-slim
WORKDIR /neural-heads
COPY setup.py ./
RUN apt-get update && apt-get install -y git
#RUN pip install torchvision 
#RUN pip install torch-geometric
#RUN pip install pytorch3d
RUN pip install torch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0
RUN pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu116
RUN pip install -e .
# Copy the rest of the application code to the container
WORKDIR /neural-heads/python_scripts
CMD ["python", "video_to_data.py"]