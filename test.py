import cv2

def open_camera(index):
    if index == 0:
        cap = cv2.VideoCapture(index, cv2.CAP_MSMF)  # Use MSMF for index 0
    else:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # Use DSHOW for other indices
    
    if cap.isOpened():
        print(f"Camera found and accessed at index {index}")
        ret, frame = cap.read()
        if ret:
            print(f"Successfully accessed frame from camera at index {index}")
        else:
            print(f"Failed to read frame from camera at index {index}")
        cap.release()
    else:
        print(f"Could not open camera at index {index}")

# Test indices 0-4
for i in range(1):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"Camera found at index {i} using DSHOW")
        cap.release()
    else:
        print(f"Could not open camera at index {i} with DSHOW")

