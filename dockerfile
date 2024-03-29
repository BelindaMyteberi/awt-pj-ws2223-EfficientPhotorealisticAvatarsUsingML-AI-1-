FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
WORKDIR /neural-heads
RUN apt-get update && apt-get install -y git ffmpeg libsm6 libxext6
RUN conda install -y -c fvcore -c iopath -c conda-forge fvcore iopath
RUN conda install -y pytorch3d=0.7.0 -c pytorch3d
RUN python -m pip install --upgrade pip
COPY setup.py ./
RUN pip install -e .
RUN pip install Flask
RUN if ! test -e deps; then mkdir -p deps; \
    git clone https://github.com/deepinsight/insightface.git deps/InsightFace; \
    git clone https://github.com/PeterL1n/RobustVideoMatting.git deps/RobustVideoMatting; \
    git clone https://github.com/boukhayma/face_normals.git deps/face_normals; \
    git clone https://github.com/zllrunning/face-parsing.PyTorch.git deps/face_parsing; \
    git clone https://github.com/philgras/video-head-tracker.git deps/video-head-tracker; \
    fi
RUN rm deps/video-head-tracker/setup.py
RUN pip install pytorch-lightning==1.9.3
ENV PATH=/usr/bin:$PATH
RUN mkdir -p static
COPY ./neural-head-avatars ./
RUN cp setup_vht.py deps/video-head-tracker/setup.py
RUN pip install -e deps/video-head-tracker
CMD ["flask", "--app", "app.py", "run", "--host", "0.0.0.0"]
