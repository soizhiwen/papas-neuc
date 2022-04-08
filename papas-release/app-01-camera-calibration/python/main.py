import sys, cv2, serial
from time import sleep
from utils import InputCamera, OutputCamera, UndistortCam
from shapedetector import ShapeDetector
from colorlabeler import ColorLabeler
from kinematics import InverseKinematics


VID_WIDTH = 1280
VID_HEIGHT = 720
VIDEO_IN = "/dev/video0"
VIDEO_OUT = "/dev/video6"

A4_X1 = 415
A4_X2 = 865
MM_TO_PIXEL = 297 / (A4_X2 - A4_X1)
OFFSET_X = 450
OFFSET_Y = 80
ORIGIN_X = 1132
ORIGIN_Y = 360


def main():
    # open and configure input camera
    input = InputCamera(VIDEO_IN, (VID_WIDTH, VID_HEIGHT))

    # open output device
    output = OutputCamera(VIDEO_OUT, (VID_WIDTH, VID_HEIGHT))

    # get undistort camera matrix
    mtx, dist, newCameraMtx, _ = UndistortCam(
        "camera.yaml", (VID_WIDTH, VID_HEIGHT)
    ).get()
    dl = []
    # loop over these actions:
    while True:
        # grab frame
        frame = input.get()

        imgUndst = cv2.undistort(frame, mtx, dist, None, newCameraMtx)
        img = cv2.cvtColor(imgUndst, cv2.COLOR_BGR2RGB)
        imgPaper = imgUndst[OFFSET_Y:640, OFFSET_X:850]
        imgBlur = cv2.GaussianBlur(imgPaper, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        imgLab = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2LAB)
        imgCanny = cv2.Canny(imgGray, 50, 50)
        contours, _ = cv2.findContours(
            imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # initialize the shape detector and color labeler
        sd = ShapeDetector()
        cl = ColorLabeler()
        # loop over the contours
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 4000 and area < 10000:
                # compute the center of the contour
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"]) + OFFSET_X
                cY = int(M["m01"] / M["m00"]) + OFFSET_Y
                # convert to end effector
                efX = ORIGIN_Y - cY
                efY = ORIGIN_X - cX
                # ef to mm
                efXMm = round(efX * MM_TO_PIXEL)
                efYMm = round(efY * MM_TO_PIXEL)
                # detect the shape of the contour and label the color
                shape = sd.detect(cnt)
                color = cl.label(imgLab, cnt)
                text = f"{color} {shape} x: {efXMm} y: {efYMm}"
                cs = f"{color}{shape}"
                if cs not in dl:
                    dl.append(cs)

                # for camera calibration, comment if unwanted
                cv2.drawContours(img, cnt, -1, (0, 255, 0), 2)
                cv2.circle(img, (cX, cY), 3, (0, 255, 0), -1)
                cv2.putText(
                    img,
                    text,
                    (cX + 10, cY + 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                )

        cv2.rectangle(
            img, (OFFSET_X, OFFSET_Y), (850, 640), (0, 255, 0), thickness=2
        )
        cv2.rectangle(img, (1145, 110), (1212, 610), (0, 255, 0), thickness=2)
        cv2.circle(img, (ORIGIN_X, ORIGIN_Y), 6, (0, 255, 0), -1)
        cv2.line(img, (400, 10), (400, 710), (0, 255, 0), 1)
        cv2.line(img, (880, 10), (880, 710), (0, 255, 0), 1)
        # write frame to output device
        output.write(img)


if __name__ == "__main__":
    sys.exit(main())
