1. Installation Steps

Step 1: Update system and install pip
sudo apt update
sudo apt install python3-pip -y
Step 2: Clone the repository
git clone https://github.com/Priyasharma04/dog_buggy.git
cd dog_buggy
Step 3: Install dependencies
pip3 install -r requirements_kit.txt

2. Configuration
Before running the project, update the following in main.py:

USE_JETSON = True

3. Running the Application

python3 main.py

4. Camera Verification

To verify camera functionality before running the full application:

python3 -c "import cv2; cap=cv2.VideoCapture(0); print(cap.isOpened())"
If the output is False, check the camera connection or configuration.

5. Performance Optimization

Reduce resolution in config.py:
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
Export the model to TensorRT for faster inference:
yolo export model=yolov5nu.pt format=engine
Then update:
MODEL_PATH = "yolov5nu.engine"