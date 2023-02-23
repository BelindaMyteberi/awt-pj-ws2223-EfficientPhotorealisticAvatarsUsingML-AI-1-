# Dynamic 4D-head avatar <br><sub>based on the following paper([Project Page](https://philgras.github.io/neural_head_avatars/neural_head_avatars.html))</sub>


Abstract: 
Within this project, we created prototype that constructs 3D avatars of a person and applies gestures to it. The prototype was created from a single video input. Through our work we aimed to use neural networks, which ensures the detection and the transfer of facial expressions from the person to a 3D avatar. During this project we explored two different approach to create a dynamic 3D avatar. One of them being NERF, making use of a neural radiance field to create an implicit 3D scene representation and Neural-Head-Avatars, based on flame mesh technology. Our final solution was based on neural-head-avatars with an integrated Application on top for an optimised user experience.

<br><br>


<br>
<br>

## Installation
For dynamic neural heads avtar:
- Install Python3.9 following the instruction on https://www.python.org/
- ```git clone --recursive https://github.com/BelindaMyteberi/awt-pj-ws2223-EfficientPhotorealisticAvatarsUsingML-AI-1-.git ```
- ```cd neural-head-avatars```
- ```pip install -e .```
- Add ```generic_model.pkl``` obtained from the [MPI website](https://flame.is.tue.mpg.de/) to ```./assets/flame```.
- Optional for training: Add the arcface model weights used for the perceptual energy term as ```backbone.pth``` to ```./assets/InsightFace```. The checkpoint can be downloaded from the [ArcFace repo](https://github.com/deepinsight/insightface/tree/c85f5399836b604611057e194a3c30230053c490/recognition/arcface_torch)
by looking for the ms1mv3_arcface_r18_fp run. To ease the search, this is the OneDrive [link](https://onedrive.live.com/?authkey=%21AFZjr283nwZHqbA&id=4A83B6B633B029CC%215578&cid=4A83B6B633B029CC) provided by their Readme. Download the ```backbone.pth``` from there.
For pre-processing your own videos:
    - Add ```rvm_mobilenetv3.pth``` obtained from [here](https://github.com/PeterL1n/RobustVideoMatting/tree/81a10937c73f68eeddb863221c61fe6a60a1cca2) to ```./assets/rvm``` for background matting ([direct link](https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3.pth)).
    - Add ```model.pth``` obtained from [here](https://github.com/boukhayma/face_normals/tree/5d6f21098b60dd5b43f82525383b2697df6e712b) to ```./assets/face_normals``` for face normal map prediction ([direct link](https://drive.google.com/file/d/1Qb7CZbM13Zpksa30ywjXEEHHDcVWHju_)).
    - Add ```model.pth``` obtained from [here](https://github.com/zllrunning/face-parsing.PyTorch/tree/d2e684cf1588b46145635e8fe7bcc29544e5537e) to ```./assets/face_parsing``` for facial segmentation ([direct link](https://drive.google.com/open?id=154JgKpzCPW82qINcVieuPH3fZ2e0P812)).
    - Run `pip install -e deps/video-head-tracker` to install the FLAME tracker.  Download the flame
     head model and texture space from the official [website](https://flame.is.tue.mpg.de/)
     and add them as ```generic_model.pkl``` and ```FLAME_texture.npz``` under ```./assets/flame```.
     Go to ```https://github.com/HavenFeng/photometric_optimization``` and copy the uv
     parametrization ```head_template_mesh.obj``` of FLAME found
     [there](https://github.com/HavenFeng/photometric_optimization/blob/master/data/head_template_mesh.obj)
     to ```./assets/flame```, as well. (This is basically what the README of the flame tracking repo
     tells you.)
<br>

## Build application
- ```docker build -t awtimage  .```
## Run application
- ```docker run awtimage```
This shoudl run in browser on port ```http://127.0.0.1:5000```

