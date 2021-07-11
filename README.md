# handwittenCalculator_tensorflow-flask
- 손글씨로 적은 사칙연산 계산식 이미지를 입력해주면 숫자와 연산자를 인식해 계산 결과를 출력해주는 프로그램입니다.
---
## 0. 계산기능 결과화면
![calc01](https://user-images.githubusercontent.com/53315807/125205229-32445480-e2bc-11eb-9d3f-9192c6b3f46a.gif)

## 1. Data
[Handwritten Math Symbols](https://www.kaggle.com/sagyamthapa/handwritten-math-symbols/code)
- image reshape : (40, 40)

## 2. Model
![스크린샷 2021-07-12 오전 3 05 30](https://user-images.githubusercontent.com/53315807/125205602-05913c80-e2be-11eb-86ac-d07f2f5c922d.png)
- validation accuracy: 0.9365
---
## Reqirements
- tensorflow==2.5.0
- opencv-python==4.5.2.54
- Flask==2.0.1
- imutils==0.5.4
