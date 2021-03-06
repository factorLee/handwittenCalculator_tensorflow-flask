##############
## utils.py ## 
##############
import cv2
import numpy as np
import imutils
from imutils.contours import sort_contours
from tensorflow.keras.models import load_model
from helper_functions import unzip_data

# read & open zipfile
# unzip_data('/Users/sangjulee1/Desktop/github/handwittenCalculator_tensorflow-flask/HandwrittenCalcApp/model/HandwrittenCalc_acc_0.9644.H5-20210719T094336Z-001.zip')

# model load
new_model = load_model('./model/HandwrittenCalc_acc_0.9644.H5')
# print("@@@@ 모델이 잘 불러와졌습니다. @@@@", new_model.summary())

# train_set.class_indices
label_map = {'%': 0, '*': 1, '+': 2, '-': 3, 
                            '0': 4, '1': 5, '2': 6, '3': 7,
                            '4': 8, '5': 9, '6': 10, '7': 11, 
                            '8': 12, '9': 13, '[': 14, ']': 15
                            }

def prediction(img):
    img = cv2.resize(img,(40, 40))  # model에 맞는 input 사이즈
    norm_image = cv2.normalize(img, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F) # alpha와 beta 구간으로 input image 정규화 (픽셀값을 고르게 펴 화질개선)
    norm_image = norm_image.reshape((norm_image.shape[0], norm_image.shape[1], 1))
    case = np.asarray([norm_image])
    pred = new_model.predict_classes([case])    # 예측한 인덱스
    return ([i for i in label_map if label_map[i]==(pred[0])][0],pred)  # class_indices의 key 값에 대한 value와 예측한 value가 같으면 i를 반환한다.


def pipeline_model(path, filename, color="bgr"):
    # step 1 : 이미지 불러오기
    img = cv2.imread(path)

    # step 2 : 이미지 그레이 스케일로 변환 및 블러처리 => 엣지 검출
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    # Contour (경계처리)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]
    
    # step 3 : 사각형 윤곽 따기
    chars=[]
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c) # 컨투어를 감싸는 최소 크기 사각형 요소 반환
        if w*h>1200:    # threshold : 1200
            roi = gray[y:y + h, x:x + w]    # ROI : 숫자 혹은 연산자만 가져온다.
            chars.append(prediction(roi))   # 예측값 리스트 저장 
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3) # 사각형 그리기 : (이미지, 시작좌표, 종료좌표, BGR, 선두께)
        # 숫자객체를 detection한 이미지를 result 폴더에 저장
        cv2.imwrite("./static/result/{}".format(filename), img)

    labels=[ i for i in label_map ]
    eq=[] # 계산에 사용되는 숫자와 연산자를 저장하는 리스트
    pos=[] # 숫자와 연산자 요소들의 총 갯수를 저장하는 리스트
    # 예측값 정리(요소 수집)
    for i in ((chars)):
        if len(eq)==0 and i[0][0] in labels[3:]:
            eq.append(i[0][0])
        elif len(eq)>0 and i[0][0] in labels[4:14]:
            eq.append(i[0][0])    
        elif len(eq)>0 and i[0][0] in labels[:4]:
            eq.append(i[0][0])
            pos.append(len(eq))
        else:
            pass

    # 계산 Loop 및 예외처리
    try:
        for i in pos:
            # if eq
            if eq[i-1]=='+':
                rightSide = int(''.join(eq[:pos[0]-1])) # 우변
                leftSide = int(''.join(eq[pos[0]:]))    # 좌변
                operator = '+'  # 연산자
                sol = rightSide + leftSide  # solution
            elif eq[i-1]=='%': 
                rightSide = int(''.join(eq[:pos[0]-1]))
                leftSide = int(''.join(eq[pos[0]:]))
                operator = '/'
                sol = rightSide / leftSide
            elif eq[i-1]=='*':
                rightSide = int(''.join(eq[:pos[0]-1]))
                leftSide = int(''.join(eq[pos[0]:]))
                operator = '*'
                sol = rightSide * leftSide
            else:
                rightSide = int(''.join(eq[:pos[0]-1]))
                leftSide = int(''.join(eq[pos[0]:]))                
                operator = '-'
                sol = rightSide - leftSide
    # 입력값 오류
    except:
        sol = 'error'    
        rightSide = 'error' 
        leftSide = 'error'
        operator = 'error'

    return sol, rightSide, leftSide, operator
