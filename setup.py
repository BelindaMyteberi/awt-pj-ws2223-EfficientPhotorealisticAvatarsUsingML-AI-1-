from setuptools import setup, find_packages

setup(
    name="nha",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "ConfigArgParse",
        "numpy==1.21",
        # "torch@https://download.pytorch.org/whl/cu113/torch-1.10.2%2Bcu113-cp39-cp39-linux_x86_64.whl",
        # "torchvision@https://download.pytorch.org/whl/cu113/torchvision-0.11.3%2Bcu113-cp39-cp39-linux_x86_64.whl",
        # "pytorch3d@https://github.com/facebookresearch/pytorch3d",
        "matplotlib",
        "tensorboard",
        "scipy",
        "opencv-python",
        "chumpy",
        "face-alignment",
        "face-detection-tflite",
        "pytorch-lightning==1.9.3",
        "lpips",
        "pytorch_msssim",
        "cpbd@git+https://github.com/wl2776/python-cpbd.git",
        "scikit-learn",
        "torchscope@git+https://github.com/Tramac/torchscope.git",
        "jupyter"
    ],
)
