import cv2
import logging


class CameraController:
    def __init__(self, config):
        self.config = config
        self.cap = None
        self._init_camera()

    def _init_camera(self):
        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.config.get("video_source", 0))
        if not self.cap.isOpened():
            raise RuntimeError("无法打开摄像头")

        # 设置分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["frame_size"][0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["frame_size"][1])

    def read(self):
        for _ in range(3):  # 最多重试3次
            ret, frame = self.cap.read()
            if ret:
                return frame
            self._init_camera()
        raise RuntimeError("无法获取摄像头画面")

    def release(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()