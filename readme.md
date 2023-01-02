Artificial Intelligence completely revolutionized our lives and allowed immense technological progress in various fields. We are approaching the next level of internet in terms of speed and interaction where Metaverse demands high fidelity and lifelike online experience. Therefore for authentic human interaction in Metaverse user avatar fidelity is paramount. Avatars do not only need to represent a person with high visual accuracy but also require expressing similar gestures, facial expressions and head poses. The purpose of this project is to research, implement and if possible, further improve existing Machine Learning methods that allow us create an avatar from a single video input as well as detect and transfer facial expressions from the person to the avatar.

Tasks:

    Research the existing state of photorealistic avatar creation from videos or images
        Familiarizing with state-of-the art papers and understanding if they are solving the problem and how
        Researching existing code bases and understanding how they can be used for the solution
    Develop a prototype that constructs 3D avatars of a person and applies gestures to it

        Implementing a prototype to create an avatar from a single video input as well as detect and transfer facial expressions from the person to the avatar

### Installation

* Clone this repository. (https://github.com/BelindaMyteberi/awt-pj-ws2223-EfficientPhotorealisticAvatarsUsingML-AI-1-.git)

* Open directory 
```
cd awt-pj-ws2223-EfficientPhotorealisticAvatarsUsingML-AI-1-/
```
* Switch to correct branch 
```
    git checkout video-input-first-attempt
```

* Install requiremnets
```
    pip install -r requirements.txt
```
* Initialise and update submodules

```
    git submodule update --init
```

* Install COLMAP. (https://colmap.github.io/install.html) for video input data preprocessing (spatial points + view direction)

	* From [nerf-pytorch](https://github.com/yenchenlin/nerf-pytorch), use `load_llff.py` to replace the example version included in this repo.
		* In `load_llff_data()`, replace `sc = 1. if bd_factor is None else 1./(bds.min() * bd_factor)` with `sc = 1./(bds.max() - bds.min())`
	* From [LLFF](https://github.com/Fyusion/LLFF), copy from `llff/poses/` the three files `colmap_read_model.py`, `colmap_wrapper.py`, and `pose_utils.py` directly into `./llff_preprocessing` (replacing existing files).
		* In `pose_utils.py` fix the imports by:
			* Commenting out `import skimage.transform`,
			* Replacing `from llff.poses.colmap_wrapper import run_colmap` with `from .colmap_wrapper import run_colmap`,
			* Replacing `import llff.poses.colmap_read_model as read_model` with `from . import colmap_read_model as read_model`.

* Rename `HashNeRF-pytorch` module to `hashnerf`

* Global search `from llff_preprocessing import gen_poses` and replace with relative path `from .llff_preprocessing import gen_poses`

* Upload example video or use existing awt.mp4

* Run (with own sample video replace "awt.mp4" with your file name and create personal config file)

```
    python3 video_input_exploration.py --config awt.txt --input awt.mp4
```







