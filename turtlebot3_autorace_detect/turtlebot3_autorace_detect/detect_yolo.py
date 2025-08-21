import os
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO

class DetectSign(Node):

    def __init__(self):
        super().__init__('detect_sign')

        self.sub_image_type = 'raw'         # 'compressed' 또는 'raw' 선택
        self.pub_image_type = 'compressed'  # 'compressed' 또는 'raw' 선택

        if self.sub_image_type == 'compressed':
            self.sub_image_original = self.create_subscription(
                CompressedImage,
                '/detect/image_input/compressed',
                self.cbFindTrafficSign,
                10
            )
        else:
            self.sub_image_original = self.create_subscription(
                Image,
                '/detect/image_input',
                self.cbFindTrafficSign,
                10
            )

        self.pub_traffic_sign = self.create_publisher(String, '/detect/traffic_sign', 10)

        if self.pub_image_type == 'compressed':
            self.pub_image_traffic_sign = self.create_publisher(
                CompressedImage,
                '/detect/image_output/compressed', 10
            )
        else:
            self.pub_image_traffic_sign = self.create_publisher(
                Image,
                '/detect/image_output', 10
            )

        self.cvBridge = CvBridge()

        # YOLO 모델 불러오기 (weights 경로 조정 필요)
        self.model_path = 'traffic_s.pt'
        self.model = YOLO(self.model_path)
        self.get_logger().info('DetectSign Node Initialized with YOLOv8')

        # 클래스별 색상 지정 (BGR 형식)
        self.class_colors = {
            'intersection': (255, 0, 0),       # 파랑
            'right': (0, 255, 0),              # 초록
            'left': (0, 0, 255),               # 빨강
            'speed_bump': (255, 255, 0),       # 하늘색
            'school_zone': (255, 0, 255),      # 자홍색
            'parking': (0, 255, 255),          # 노랑
            'stop': (128, 0, 128),             # 보라
            'pedestrian': (0, 128, 255),       # 주황
            'speed_limit_30': (128, 128, 0),   # 카키
            'speed_limit_100': (0, 128, 128),  # 청록
            'crosswalk': (128, 0, 0),          # 진빨강
        }

    def cbFindTrafficSign(self, msg):
        # 이미지 메시지 -> OpenCV 이미지 변환
        if self.sub_image_type == 'compressed':
            np_arr = np.frombuffer(msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        else:
            cv_image = self.cvBridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # YOLOv8 모델로 객체 탐지 수행
        results = self.model(cv_image)

        boxes = results[0].boxes  # Boxes 객체

        for box in boxes:
            xyxy = box.xyxy[0].cpu().numpy().astype(int)  # [x1, y1, x2, y2]
            conf = box.conf[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())

            class_name = self.model.names[cls]

            # 클래스별 색상 가져오기 (기본값: 흰색)
            color = self.class_colors.get(class_name, (255, 255, 255))

            # 바운딩 박스 및 클래스명 그리기
            cv2.rectangle(cv_image, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
            # 클래스명 표시
            cv2.putText(cv_image, class_name, (xyxy[0], xyxy[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            # 신뢰도 표시
            cv2.putText(cv_image, f'{conf:.2f}', (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # 클래스명 발행 (첫 객체만)
            self.pub_traffic_sign.publish(String(data=class_name))
            break

        # 결과 이미지 발행
        if self.pub_image_type == 'compressed':
            msg_out = CompressedImage()
            msg_out.format = 'jpeg'
            msg_out.data = np.array(cv2.imencode('.jpg', cv_image)[1]).tobytes()
        else:
            msg_out = self.cvBridge.cv2_to_imgmsg(cv_image, encoding='bgr8')

        self.pub_image_traffic_sign.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = DetectSign()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()