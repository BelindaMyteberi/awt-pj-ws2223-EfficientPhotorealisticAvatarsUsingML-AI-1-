import os
import zipfile
import time
import sys
import ast
import configparser
import numpy as np
import torch
from io import BytesIO
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, flash, redirect, send_from_directory, send_file
from python_scripts.video_to_dataset import Video2DatasetConverter
sys.path.append("deps/video-head-tracker/")
from vht.model.tracking import FlameTracker as Tracker
from vht.data.video import VideoDataset
from vht.util.log import get_logger
sys.path.remove("deps/video-head-tracker/")


from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = b'nsjcnndcj'

ALLOWED_EXTENSIONS = {'mp4'}
UPLOAD_FOLDER = 'static/'

def allowed_file(filename):
    # xxx.mp4
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/render')
def render_form():
    if os.path.isfile('./static/awtApp/transforms.json'):
        return render_template('renderAvatar.html')
    return render_template('errorNoPp.html', missingPP=True)

@app.route('/reenact')
def reenact():
    if os.path.isfile('./static/awtOutput/optimized_avatar/lightning_logs/version_0/checkpoints/last.ckpt'):
        return render_template('reenactAvatar.html')
    return render_template('errorNoPp.html', missingPP=False, missingRender=True)

@app.route('/reenact', methods=['POST'])
def reenact_avatar():
    # Get the data from the form
    from expressions import synthesize_novel_poses_and_expressions
    if request.method == "POST":
        e0 = int(request.form["e0"])
        e1 = int(request.form["e1"])
        e2 = int(request.form["e2"])
        e3 = int(request.form["e3"])
        e4 = int(request.form["e4"])

        rot0 = int(request.form["rot0"])
        rot1 = np.pi
        rot2 = int(request.form["rot2"])


        neck0 = int(request.form["neck0"])
        neck1 = int(request.form["neck1"])
        neck2 = int(request.form["neck2"])

        jaw = 0

        expr = torch.zeros(100, dtype=torch.float)
        pose = torch.zeros(15, dtype=torch.float)
        expr[0] = e0; expr[1] = e1; expr[2] = e2; expr[3] = e3; expr[4] = e4
        pose[0] = rot0; pose[1] = rot1;  pose[2] = rot2; pose[3] = neck0;  pose[4] = neck1; pose[5] = neck2; pose[6] = jaw

        plt.switch_backend('Agg')
        rgba, shaded_mesh = synthesize_novel_poses_and_expressions(expr=expr, pose=pose, image_size=(512,512))
        fig, axes = plt.subplots(ncols=2, figsize=(20,10))
        axes[0].imshow(rgba[0,:3].cpu().permute(1,2,0))
        axes[1].imshow(shaded_mesh[0, :3].cpu().permute(1,2,0))
        [a.axis("off") for a in axes]
        plt.savefig('./static/expression.png')
        return render_template('expressionView.html')

@app.route('/render', methods=['POST'])
def render_avatar():
    # Get the data from the form
    if request.method == "POST":
        
        n_shape = int(request.form["n_shape"])
        n_expr = int(request.form["n_expr"])
        n_tex = int(request.form["n_tex"])
        device = request.form["device"]
        ignore_lower_neck = isinstance(request.form["ignore_lower_neck"], bool)
        img_log_freq = int(request.form["img_log_freq"])
        energy_log_freq = int(request.form["energy_log_freq"])
        keyframes = request.form["keyframes"]
        keyframes = ast.literal_eval(keyframes)
        init_steps = int(request.form["init_steps"])
        steps_per_frame = int(request.form["steps_per_frame"])
        sub_steps = int(request.form["sub_steps"])
    
    # Save the data to the file
        with open("tracking.ini", "w") as f:
            f.write("[dataset]\n")
            f.write("data_path = ./static/awtApp\n\n")
            f.write("[model]\n")
            f.write(f"n_shape = {n_shape}\n")
            f.write(f"n_expr = {n_expr}\n")
            f.write(f"n_tex = {n_tex}\n")
            f.write("tex_res = 512\n\n")
            f.write("[training]\n")
            f.write(f"device = {device}\n")
            f.write(f"ignore_lower_neck = {ignore_lower_neck}\n")
            f.write(f"img_log_freq = {img_log_freq}\n")
            f.write(f"keyframes = {keyframes}\n")
            f.write("[hyper params]\n")
            f.write(f"energy_log_freq = {energy_log_freq}\n")
            f.write(f"init_steps = {init_steps}\n")
            f.write(f"steps_per_frame = {steps_per_frame}\n")
            f.write(f"sub_steps = {sub_steps}\n")
            f.write("lr = 0.005\n")
            f.write("pos_lr = 0.001\n")
            f.write("light_lr = 0.005\n")
            f.write("cam_lr = 0.005\n\n")
            f.write("blur_sigma = [10, 1e-4]\n")
            f.write("sampling_scale = 4\n\n")
            f.write("# loss weights\n")
            f.write("w_lmk = 5\n")
            f.write("w_eyes_sym = 10\n")
            f.write("w_eyes_lmk = 2\n")
            f.write("w_photo = 30\n\n")
            f.write("w_expr_reg = 1e-3\n")
            f.write("w_shape_reg = 1e-3\n")
            f.write("w_tex_reg = 1e-3\n\n")
            f.write("w_pos_glob = 1e-2\n")
            f.write("w_pos_neck = 1e-2\n")
            f.write("w_pos_jaw = 1e-4\n")
            f.write("w_pos_eyes = 1e-4\n")
            f.write("w_pos_trans = 10")

    # Render a success message or redirect to another page
    args_dic = {
        "calibrated": False,
        "load_tracked_flame_params": None,
        "lr": 0.005,
        "pos_lr": 0.001,
        "cam_lr": 0.005,
        "light_lr": 0.005,
        "w_lmk": 5.0,
        "w_photo": 30.0,
        "w_shape_reg": 0.001,
        "w_expr_reg": 0.001,
        "w_tex_reg": 0.001,
        "w_pos_trans": 10.0,
        "w_pos_glob": 0.01,
        "w_pos_neck": 0.01,
        "w_pos_jaw": 0.0001,
        "w_pos_eyes": 0.0001,
        "w_eyes_sym": 10.0,
        "w_eyes_lmk": 2.0,
        "blur_sigma": [10.0, 0.0001],
        "sampling_scale": 4.0,
        "n_shape": n_shape,
        "n_expr": n_expr,
        "n_tex": n_tex,
        "tex_res": 512,
        "ignore_lower_neck": ignore_lower_neck,
        "steps_per_frame": steps_per_frame,
        "sub_steps": sub_steps,
        "init_steps": init_steps,
        "img_log_freq": img_log_freq,
        "energy_log_freq": energy_log_freq,
        "output_path": "./static/awtOutput",
        "save_period": 1,
        "device": device,
        "keyframes": keyframes,
        "cutframes": (),
        "frame_rate": 30,
        "config": "configs/tracking.ini",
        "data_path": "./static/awtApp",
        "video": None,
        "downscale_factor": 1.0
    }


    data = VideoDataset("./static/awtApp", 1.0)
    tracker = Tracker(data, **args_dic)
    tracker.optimize()
    video = True
    return render_template('renderAvatarOptput.html', video=video)





@app.route('/', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No mp4 selected for uploading')
        return redirect(request.url)
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/', filename))
        converter = Video2DatasetConverter(
            os.path.join('static/', filename),
            "static/awtApp",
            512,
            False,
            False
        )
        converter.extract_frames()
        converter.apply_transforms(crop_seg=False, pad_to_square=False)
        converter.annotate_landmarks()
        converter.annotate_parsing()
        converter.annotate_segmentation()
        converter.annotate_face_normals()
        return render_template('upload.html', filename=filename)


@app.route("/display/<path:filename>")
def display_video(filename):
    return send_from_directory('static/', filename, as_attachment=True
    )

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(threaded=True)

@app.route('/download-zip')
def request_zip():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "my_data_preprocd{}.zip".format(timestr)
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
          for root, dirs, files in os.walk('static'):
                    for file in files:
                              zipf.write(os.path.join(root, file))
    memory_file.seek(0)
    return send_file(memory_file,
                     download_name=fileName,
                     as_attachment=True)

@app.route('/download-zip-avatar')
def request_zip_avatar():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "my_avatar{}.zip".format(timestr)
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
          for root, dirs, files in os.walk('static/awtOutput'):
                    for file in files:
                              zipf.write(os.path.join(root, file))
    memory_file.seek(0)
    return send_file(memory_file,
                     download_name=fileName,
                     as_attachment=True)
