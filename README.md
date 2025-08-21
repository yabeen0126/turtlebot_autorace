# 🤖 차선인식 기반 자율주행 로봇 (ROKEYBOT)
![작동 영상](https://github.com/I5-BatteryCheck/.github/blob/main/profile/i5-readme-video.gif)
---

## 📄프로젝트 개요
카메라 기반 시각 인식 기술의 중요성이 증대됨에 따라, TurtleBot3와 ROS2를 활용하여 영상 처리 기반의 차선 인식 알고리즘을 개발함. 이를 통해 로봇의 자율주행 및 특정 작업 수행을 위한 기초 기술을 구현하는 것이 본 프로젝트의 목표임.

---

## 🔍 Architecture

![ROS Node Architecture](https://user-images.githubusercontent.com/12345678/your-image-link-here.png)
*<-- ROS Node Architecture 다이어그램 이미지 삽입 영역*


---


### 📅 개발기간
- 2024.06.09 ~ 2024.06.20

---

## 🧑 팀원
- **백홍하(팀장)**: ARUCO 마커 관련 로직, Manipulation
- **이하빈**: 차선 탐지 및 경로 로직
- **장연호**: 차선 탐지 및 경로 로직
- **정찬원**: 터틀봇 이동 로직, Manipulation

---

## ⚙️ 개발 환경
### 🤖 Robotics & Hardware
![RASPBERRY PI](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white) ![NVIDIA](https://img.shields.io/badge/Nvidia%20Jetson%20Nano-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
- **Robot**: TurtleBot3 Waffle Pi
- **Camera**: DRGO Webcam
- **Actuator**: Dynamixel
- **Manipulator**: OpenMANIPULATOR-X

### 💻 Software & AI
![PYTHON](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) <img src="https://img.shields.io/badge/ROS2%20Humble-5A7594?style=for-the-badge&logo=ros&logoColor=white"> <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">
- **Frameworks**: ROS2 Humble
- **Key Libraries**: rclpy, numpy, OpenCV
- **Markers**: Aruco Marker

---

## 📐 Diagrams

### ER Diagram
![ER Diagram](https://user-images.githubusercontent.com/12345678/your-image-link-here.png)
*<-- ERD 이미지 삽입 영역*

### UML Class Diagram
![UML Diagram](https://user-images.githubusercontent.com/12345678/your-image-link-here.png)
*<-- UML 이미지 삽입 영역*

---

## ⭐ 주요 기능

- **차선 인식 기반 자율 주행**
  - **이미지 전처리**: 입력된 카메라 영상의 원근 왜곡을 제거하기 위해 조감도(Bird's Eye View) 변환을 적용함. 조명 변화에 강건하게 대응하고자 HSV 색 공간 변환 및 CLAHE(Contrast Limited Adaptive Histogram Equalization)를 통해 명암 대비를 개선하였음.
  - **차선 검출**: 흰색과 노란색 차선을 HSV 임계값으로 필터링하여 마스크를 생성함. 빛 반사 등으로 발생하는 노이즈는 레이블링 기법을 통해 가장 큰 면적의 객체만 유지하는 방식으로 제거함.
  - **경로 생성 및 주행 제어**: 검출된 차선 픽셀에 2차 다항식을 피팅(Polyfit)하여 주행 경로를 추정함. 로봇의 현재 위치와 목표 경로 중심 간의 오차를 기반으로 PD 제어기를 사용하여 선속도와 각속도를 제어, 안정적인 차선 추종 주행을 구현하였음.

- **Aruco 마커 인식 및 Manipulation**
  - **마커 검출 및 위치 추정**: 트랙 위의 Aruco 마커를 실시간으로 탐지하고, 카메라 좌표계에서 로봇 베이스 좌표계로 위치를 변환하여 마커까지의 정확한 거리와 위치를 계산함.
  - **자동화된 작업 수행**: 마커와의 거리에 따라 로봇의 감속 및 정지 상태를 제어함. 정지 후에는 OpenMANIPULATOR-X를 이용해 마커를 집고(Pick) 지정된 위치로 옮기는(Place) 작업을 수행하며, 완료 시 주행을 재개함.

---

## 🎬 프로젝트 결과물
### 차선 인식 및 주행 화면
![차선인식 화면](https://user-images.githubusercontent.com/12345678/your-image-link-here.png)
*<-- 차선 인식 및 주행 테스트 결과 이미지 삽입 영역*

### Aruco 마커 인식 및 조작
![마커인식 화면](https://user-images.githubusercontent.com/12345678/your-image-link-here.png)
*<-- Aruco 마커 인식 및 Manipulation 결과 이미지 삽입 영역*
