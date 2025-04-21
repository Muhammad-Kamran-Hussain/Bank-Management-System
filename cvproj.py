import os
import re
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

output_dir = 'detected'
os.makedirs(output_dir, exist_ok=True)

col_frames = os.listdir('frames/content')

col_frames.sort(key=lambda f: int(re.sub('\D', '', f)) if re.sub('\D', '', f) else 0)

col_images = []
for i in tqdm(col_frames):
    img_path = os.path.join('frames\content', i)  # Specify the path to your frames directory
    img = cv2.imread(img_path)
    if img is None:
        print(f"Failed to load image: {img_path}")
    else:
        col_images.append(img)

idx = 100
plt.figure(figsize=(10, 10))
plt.imshow(col_images[idx][:, :, 0], cmap="gray")
plt.show()

stencil = np.zeros_like(col_images[idx][:, :, 0])
polygon = np.array([[50, 270], [220, 160], [360, 160], [480, 270]])
cv2.fillConvexPoly(stencil, polygon, 1)

plt.figure(figsize=(10, 10))
plt.imshow(stencil, cmap="gray")
plt.show()

img = cv2.bitwise_and(col_images[idx][:, :, 0], col_images[idx][:, :, 0], mask=stencil)
plt.figure(figsize=(10, 10))
plt.imshow(img, cmap="gray")
plt.show()

ret, thresh = cv2.threshold(img, 130, 145, cv2.THRESH_BINARY)
plt.figure(figsize=(10, 10))
plt.imshow(thresh, cmap="gray")
plt.show()

lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 30, maxLineGap=200)
dmy = col_images[idx][:, :, 0].copy()
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(dmy, (x1, y1), (x2, y2), (255, 0, 0), 3)
plt.figure(figsize=(10, 10))
plt.imshow(dmy, cmap="gray")
plt.show()

cnt = 0

for img in tqdm(col_images):
    masked = cv2.bitwise_and(img[:, :, 0], img[:, :, 0], mask=stencil)
    ret, thresh = cv2.threshold(masked, 130, 145, cv2.THRESH_BINARY)
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 30, maxLineGap=200)
    dmy = img.copy()
    try:
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(dmy, (x1, y1), (x2, y2), (255, 0, 0), 3)

        output_file = os.path.join(output_dir, f'{cnt}.png')
        success = cv2.imwrite(output_file, dmy)
        if not success:
            print(f"Failed to save image: {output_file}")
    except TypeError:
        output_file = os.path.join(output_dir, f'{cnt}.png')
        success = cv2.imwrite(output_file, img)
        if not success:
            print(f"Failed to save image: {output_file}")

    cnt += 1

pathIn = 'detected/'
pathOut = 'roads_v2.mp4'
fps = 30.0

if not os.path.exists(pathIn):
    os.makedirs(pathIn)
    print("Directory 'detected/' created.")
else:
    print("Directory 'detected/' already exists.")

files = [f for f in os.listdir(pathIn) if os.path.isfile(os.path.join(pathIn, f))]
files.sort(key=lambda f: int(re.sub('\D', '', f)))

frame_list = []
for file in files:
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
