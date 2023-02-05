import sys
import torch
import configargparse

from nonrigid_nerf.preprocess import preprocess

sys.path.append("./hashnerf")

from hashnerf import run_nerf

def main():
    parser = run_nerf.config_parser()
    parser.add_argument(
        "--input",
        type=str,
        help='input. can be a video file or folder that contains a subfolder named "images", which contains images. e.g. set to foo/bar if images are in foo/bar/images/image0.png',
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help='custom output folder. similar to --input, needs to be foo/bar such that subfolders like "images" can be created as foo/bar/images/',
    )
    parser.add_argument(
        "--calibrate_lens_distortion",
        action="store_true",
        help="computes lens distortion parameters to later undistort images. input sequence needs to contain a checkerboard that follows the OpenCV design. does not compute camera poses.",
    )
    parser.add_argument(
        "--undistort_with_calibration_file",
        type=str,
        default=None,
        help="path to lens_distortion.json, the lens distortion calibration file (computed with calibrate_lens_distortion) that will be used to undistort the input images before running colmap.",
    )
    parser.add_argument(
        "--colmap_matching",
        type=str,
        default="sequential_matcher",
        help='"sequential_matcher" (default. for temporally ordered input, e.g. video) or "exhaustive_matcher" (each image is matched with every other image).',
    )
    parser.add_argument(
        "--ffmpeg_path",
        type=str,
        default="ffmpeg",
        help="path to ffmpeg executable. only used for video input.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=5,
        help="when using video input, the frame rate at which images should be extracted from the video",
    )
    args = parser.parse_args()
    preprocess(args)

    #remove --index because run_nerf.train() complains. There may be a better solution.
    input_argument_index = sys.argv.index("--input")
    sys.argv.pop(input_argument_index)
    sys.argv.pop(input_argument_index)

    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    run_nerf.train()


main()