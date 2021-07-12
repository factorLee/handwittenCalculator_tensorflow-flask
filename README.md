
# handwittenCalculator_tensorflow-flask
- *손글씨로 적은 사칙연산 계산식 이미지를 입력해주면 숫자와 연산자를 인식해 계산 결과를 출력해주는 프로그램입니다.*
---
## 0. 계산기능 결과화면
![calc01](https://user-images.githubusercontent.com/53315807/125205229-32445480-e2bc-11eb-9d3f-9192c6b3f46a.gif)

## 1. Data
[Handwritten Math Symbols](https://www.kaggle.com/sagyamthapa/handwritten-math-symbols/code)
- 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, add, div, mul, sub

[Dataset: Handwritten Digits and Operators](https://www.kaggle.com/michelheusser/handwritten-digits-and-operators)
- %, *, +, -, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, [, ]

## 2. Input
- shape : (40, 40)
- (입력 샘플사진)

![sample input](https://user-images.githubusercontent.com/53315807/125338743-866a3a00-e38b-11eb-886a-421b7bd9216e.png)



## 3. Model
- layers

![layers](https://user-images.githubusercontent.com/53315807/125338413-1c519500-e38b-11eb-8d33-62d4d0163a92.png)

- optimizer : Adam
- loss : Categorical Crossentropy
- epoch : 20
- batch_size : 256
- validation accuracy : ~~0.8957~~ -> ~~0.9365~~ -> ~~0.9456~~ -> ~~0.9515(목표치)~~ -> **0.9531**(개선중)

## 4. Recognition
- (ROI 인식 샘플사진)

![ROI Recognition sample image](https://user-images.githubusercontent.com/53315807/125338855-ad287080-e38b-11eb-8717-11a42669a1d8.png)

## 5. Output
- (output image sample)


![output image sample](https://user-images.githubusercontent.com/53315807/125338977-d3e6a700-e38b-11eb-8a72-dc88f51eed6d.png)


---
## Reqirements
- tensorflow==2.5.0
- opencv-python==4.5.2.54
- Flask==2.0.1
- imutils==0.5.4


## Reference
[reference1](https://www.kaggle.com/rohankurdekar/handwritten-basic-math-equation-solver)
