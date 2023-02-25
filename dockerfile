FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime
WORKDIR /neural-heads
COPY setup.py ./
COPY ./neural-head-avatars ./
RUN apt-get update && apt-get install -y git ffmpeg libsm6 libxext6
RUN conda install -y -c fvcore -c iopath -c conda-forge fvcore iopath
RUN conda install -y pytorch3d=0.7.2 -c pytorch3d
RUN python -m pip install --upgrade pip
RUN pip install tensorflow==2.7.4
RUN pip install -e .
RUN pip install Flask
RUN pip install -e deps/video-head-tracker
RUN pip install pytorch-lightning==1.9.3
RUN export PATH=/usr/bin:$PATH
CMD ["flask", "--app", "app.py", "run", "--host", "0.0.0.0"]