from flask import Flask, request, render_template, send_file
import os
import re
import cv2
import numpy as np
from tqdm import tqdm

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_DIR = 'detected'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024




def process_images():
    col_frames = os.listdir(UPLOAD_FOLDER)
    col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

    stencil = np.zeros((480, 640), dtype=np.uint8)
    polygon = np.array([[50, 270], [220, 160], [360, 160], [480, 270]])
    cv2.fillConvexPoly(stencil, polygon, 1)

    cnt = 0
    for file in tqdm(col_frames):
        img_path = os.path.join(UPLOAD_FOLDER, file)
        img = cv2.imread(img_path)
        if img is not None:
            masked = cv2.bitwise_and(img[:, :, 0], img[:, :, 0], mask=stencil)
            ret, thresh = cv2.threshold(masked, 130, 145, cv2.THRESH_BINARY)
            lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 30, maxLineGap=200)
            dmy = img.copy()
            try:
                if lines is not None:
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        cv2.line(dmy, (x1, y1), (x2, y2), (255, 0, 0), 3)
                output_file = os.path.join(OUTPUT_DIR, f'{cnt}.png')
                success = cv2.imwrite(output_file, dmy)
                if not success:
                    print(f"Failed to save image: {output_file}")
            except TypeError:
                output_file = os.path.join(OUTPUT_DIR, f'{cnt}.png')
                success = cv2.imwrite(output_file, img)
                if not success:
                    print(f"Failed to save image: {output_file}")
            cnt += 1

def create_video():
    pathIn = OUTPUT_DIR
    pathOut = 'roads_v2.mp4'
    fps = 30.0
    files = [f for f in os.listdir(pathIn) if os.path.isfile(os.path.join(pathIn, f))]
    files.sort(key=lambda f: int(re.sub('\D', '', f)))

    frame_list = []
    for file in tqdm(files):
        img_path = os.path.join(pathIn, file)
        img = cv2.imread(img_path)
        if img is not None:
            frame_list.append(img)
    
    out = None
    for frame in frame_list:
        if out is None:
            height, width, _ = frame.shape
            size = (width, height)
            out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
            if out is None:
                print("Error creating VideoWriter object. Check output path and codec.")
                break
        out.write(frame)
    if out is not None:
        out.release()
    return pathOut

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
        process_images()
        video_path = create_video()
        return render_template('download.html', video_path=video_path)
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
