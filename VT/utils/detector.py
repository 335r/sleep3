import torch
import json
import numpy as np
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords, letterbox


class YOLOv7Detector:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)

        # 初始化设备
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 加载模型
        self.model = attempt_load('weights/yolov7.pt', map_location=self.device)
        self.stride = int(self.model.stride.max())
        self.img_size = check_img_size(self.config["img_size"], s=self.stride)
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names

        # 优化配置
        if self.device.type != 'cpu':
            self.model.half()
            self.model(torch.zeros(1, 3, self.img_size, self.img_size))

    def detect(self, frame):
        img = self._preprocess(frame)
        with torch.no_grad():
            pred = self.model(img)[0]

        pred = non_max_suppression(
            pred, self.config["conf_thres"],
            self.config["iou_thres"],
            classes=self.config.get("classes"),
            agnostic=self.config["agnostic_nms"]
        )

        detections = []
        for det in pred:
            if det is not None:
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
                detections.append(det.cpu().numpy())
        return detections

    def _preprocess(self, frame):
        img = letterbox(frame, self.img_size, stride=self.stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR转RGB
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.device.type != 'cpu' else img.float()
        img /= 255.0
        return img.unsqueeze(0)