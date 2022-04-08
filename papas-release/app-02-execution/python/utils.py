import os, fcntl, uuid, cv2, queue, threading
from v4l2 import (
    v4l2_format,
    VIDIOC_G_FMT,
    V4L2_BUF_TYPE_VIDEO_OUTPUT,
    V4L2_PIX_FMT_RGB24,
    V4L2_FIELD_NONE,
    VIDIOC_S_FMT,
)


class InputCamera:
    def __init__(self, path, size):
        self.dev = cv2.VideoCapture(path)
        if not self.dev.isOpened():
            raise RuntimeError("could not open camera")
        self.dev.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.dev.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        # Uncomment if 1080p
        # self.dev.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.dev.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def get(self):
        return self.q.get()


class OutputCamera:
    def __init__(self, path, size):
        try:
            self.dev = os.open(path, os.O_RDWR)
        except Exception:
            raise RuntimeError("could not open output device!")

        vid_format = v4l2_format()
        vid_format.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
        if fcntl.ioctl(self.dev, VIDIOC_G_FMT, vid_format) < 0:
            raise RuntimeError("unable to get output video format")

        framesize = size[0] * size[1] * 3
        vid_format.fmt.pix.width = size[0]
        vid_format.fmt.pix.height = size[1]
        vid_format.fmt.pix.pixelformat = V4L2_PIX_FMT_RGB24
        vid_format.fmt.pix.sizeimage = framesize
        vid_format.fmt.pix.field = V4L2_FIELD_NONE

        if fcntl.ioctl(self.dev, VIDIOC_S_FMT, vid_format) < 0:
            raise RuntimeError("unable to set output video format")

    def write(self, frame):
        if os.write(self.dev, frame.data) < 0:
            raise RuntimeError("could not write to output device")

class UndistortCam:
    def __init__(self, path, size):
        fs = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
        # camera_matrix
        self.mtx = fs.getNode("K")
        self.mtx = self.mtx.mat()
        # distortion_coefficients
        self.dist = fs.getNode("D")
        self.dist = self.dist.mat()

        self.newCameraMtx, self.roi = cv2.getOptimalNewCameraMatrix(
            self.mtx, self.dist, size, 1, size
        )

    def get(self):
        return self.mtx, self.dist, self.newCameraMtx, self.roi
