import cv2

def draw(frame, detections, owner):
    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        color = (0,255,0)

        if owner and d == owner:
            color = (0,0,255)  # RED → owner
        else:
            color = (0,255,0)

        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)

    return frame
