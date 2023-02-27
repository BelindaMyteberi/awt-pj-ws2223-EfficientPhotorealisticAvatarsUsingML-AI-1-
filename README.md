# Dynamic 4D-head avatar <br><sub>based on the following paper([Project Page](https://philgras.github.io/neural_head_avatars/neural_head_avatars.html))</sub>


Abstract: 
Within this project, we created prototype that constructs 3D avatars of a person and applies gestures to it. The prototype was created from a single video input. Through our work we aimed to use neural networks, which ensures the detection and the transfer of facial expressions from the person to a 3D avatar. During this project we explored two different approach to create a dynamic 3D avatar. One of them being NERF, making use of a neural radiance field to create an implicit 3D scene representation and Neural-Head-Avatars, based on flame mesh technology. Our final solution was based on neural-head-avatars with an integrated Application on top for an optimised user experience.

<br><br>


<br>
<br>

## Dependencies
For dynamic neural heads avtar:
- Install Python3.9 following the instruction on https://www.python.org/
- ```git clone --recursive https://github.com/BelindaMyteberi/awt-pj-ws2223-EfficientPhotorealisticAvatarsUsingML-AI-1-.git ```
- Add ```generic_model.pkl``` obtained from the [MPI website](https://flame.is.tue.mpg.de/) to ```./assets/flame```.
- Optional for training: Add the arcface model weights used for the perceptual energy term as ```backbone.pth``` to ```./assets/InsightFace```. The checkpoint can be downloaded from the [ArcFace repo](https://github.com/deepinsight/insightface/tree/c85f5399836b604611057e194a3c30230053c490/recognition/arcface_torch)
by looking for the ms1mv3_arcface_r18_fp run. To ease the search, this is the OneDrive [link](https://onedrive.live.com/?authkey=%21AFZjr283nwZHqbA&id=4A83B6B633B029CC%215578&cid=4A83B6B633B029CC) provided by their Readme. Download the ```backbone.pth``` from there.
For pre-processing your own videos:
    - Add ```rvm_mobilenetv3.pth``` obtained from [here](https://github.com/PeterL1n/RobustVideoMatting/tree/81a10937c73f68eeddb863221c61fe6a60a1cca2) to ```./assets/rvm``` for background matting ([direct link](https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3.pth)).
    - Add ```model.pth``` obtained from [here](https://github.com/boukhayma/face_normals/tree/5d6f21098b60dd5b43f82525383b2697df6e712b) to ```./assets/face_normals``` for face normal map prediction ([direct link](https://drive.google.com/file/d/1Qb7CZbM13Zpksa30ywjXEEHHDcVWHju_)).
    - Add ```79999_iter.pth``` obtained from [here](https://github.com/zllrunning/face-parsing.PyTorch/tree/d2e684cf1588b46145635e8fe7bcc29544e5537e) to ```./assets/face_parsing``` for facial segmentation ([direct link](https://drive.google.com/open?id=154JgKpzCPW82qINcVieuPH3fZ2e0P812)).
    -Download the flame texture space from the official [website](https://flame.is.tue.mpg.de/)
     and add it as ```FLAME_texture.npz``` under ```./assets/flame```.
     Go to ```https://github.com/HavenFeng/photometric_optimization``` and copy the uv
     parametrization ```head_template_mesh.obj``` of FLAME found
     [there](https://github.com/HavenFeng/photometric_optimization/blob/master/data/head_template_mesh.obj)
     to ```./assets/flame```, as well. (This is basically what the README of the flame tracking repo tells you excluding the actual installation.)
<br>

## Build application
- ```docker build -t awtimage  .```
## Run application
- Use the paramter ```--ipc=host``` or ```--shm-size="desired amount of memory"``` depending on your hardware.
- e.g. ```docker run --gpus all --ipc=host -p 5000:5000 awtimage```
This should run in your browser at ```localhost:5000```

## Acknowledgements

This work is heavily inspired by the [Neural Head Avatars from Monocular RGB Videos](https://github.com/philgras/neural-head-avatars) repository by Philip-William Grassal, Malte Prinzler, Titus Leistner, Carsten Rother, Matthias Nie{\ss}ner, and Justus Thies. Please note that the use and distribution of neural head code is subject to the CC BY-NC 3.0 license. 
Another project that inspired us is the work of HavenFeng [2], whose code for photometric optimization can be found at https://github.com/HavenFeng/photometric_optimization. The files flame.py and lbs.py in this project are property of the Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. and are adapted from the work of HavenFeng [2].
In addition, the FLAME head model [4] was used in this project. The files in the ./assets directory are adapted from the FLAME head model, and the license for the FLAME head model can be found at [4].

- [1] Philip-William Grassal, Malte Prinzler, Titus Leistner, Carsten Rother, Matthias Nie{\ss}ner, and Justus Thies. Neural Head Avatars from Monocular RGB Videos https://github.com/philgras/neural-head-avatars 
- [2] HavenFeng. Photometric optimization. https://github.com/HavenFeng/photometric_optimization.
- [3] Li, Tianye, Timo Bolkart, Michael J. Black, Hao Li, and Javier Romero. "Learning a model of facial shape and expression from 4D scans." ACM Transactions on Graphics (TOG) 36, no. 6 (2017): 194.
- [4] The FLAME model. http://flame.is.tue.mpg.de/.


# LICENSE
This code is released under the MIT License. See the LICENSE file for more information: https://github.com/BelindaMyteberi/awt-pj-ws2223-EfficientPhotorealisticAvatarsUsingML-AI-1-/blob/main/License




