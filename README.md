# ROAD LANE DETECTION

This repository contains a Flask web application designed for processing images and creating a video from the processed frames. The project focuses on detecting and drawing lines on images, typically representing roads or lanes, using computer vision techniques. The processed images are then compiled into a video.

## Features

- **Image Upload**: Users can upload a series of images through a web interface.
- **Image Processing**: Each uploaded image undergoes a process to detect and highlight lines (such as road lanes) using OpenCV.
- **Video Creation**: The processed images are compiled into a video, which can be downloaded by the user.
- **File Management**: Uploaded images and processed outputs are stored in specific directories.

## Project Structure

- **app.py**: The main Flask application file. It handles the web routes, file uploads, image processing, and video creation.
- **uploads/**: Directory where uploaded images are stored.
- **detected/**: Directory where processed images are stored.
- **templates/**: Contains the HTML templates for the web interface.
  - `upload.html`: The main page where users can upload their images.
  - `download.html`: The page from which users can download the processed video.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/cv-lab-project.git
   cd cv-lab-project
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1. **Upload Images**: On the main page, select and upload the images you want to process.
2. **Processing**: After uploading, the application will automatically process the images to detect lines and highlight them.
3. **Download Video**: Once processing is complete, a video compiled from the processed images will be available for download.

## Dependencies

- Flask: A web framework for Python.
- OpenCV: A library for computer vision tasks.
- TQDM: A library for showing progress bars in the terminal.
