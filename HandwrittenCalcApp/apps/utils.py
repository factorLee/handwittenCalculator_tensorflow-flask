import cv2
import numpy as np
import imutils
from imutils.contours import sort_contours
from tensorflow.keras.models import load_model
from helper_functions import unzip_data

# read & open zipfile
# unzip_data('/Users/sangjulee1/Documents/flask_tensorflow_practice/HandwrittenCalc_acc_93.H5-20210707T153038Z-001.zip')

# model load
new_model = load_model('./model/HandwrittenCalc_acc_93.H5')
print("@@@@ 모델이 잘 불러와졌습니다. @@@@", new_model.summary())

# train_set.class_indices
label_map = {'%': 0, '*': 1, '+': 2, '-': 3, 
                            '0': 4, '1': 5, '2': 6, '3': 7,
                            '4': 8, '5': 9, '6': 10, '7': 11, 
                            '8': 12, '9': 13, '[': 14, ']': 15
                            }

def prediction(img):
    img = cv2.resize(img,(40, 40))
    norm_image = cv2.normalize(img, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    norm_image = norm_image.reshape((norm_image.shape[0], norm_image.shape[1], 1))
    case = np.asarray([norm_image])
    pred = new_model.predict_classes([case])    # 예측한 인덱스
    return ([i for i in label_map if label_map[i]==(pred[0])][0],pred)  # class_indices의 key 값에 대한 value와 예측한 value가 같으면 i를 반환한다.


def pipeline_model(path, filename, color="bgr"):
    # step 1 : 이미지 불러오기
    img = cv2.imread(path)

    # step 2 : 이미지 그레이 스케일로 변환 및 블러처리 => 경계선 추출
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]
    
    # step 3 : 사각형 윤곽 따기
    chars=[]
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c) # 컨투어를 둘러싸는 윤곽선 박스
        if w*h>1200:
            roi = gray[y:y + h, x:x + w]
            chars.append(prediction(roi))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # (이미지, 시작좌표, 종료좌표, BGR, 선두께)
        # 숫자객체를 detection한 이미지를 result 폴더에 저장
        cv2.imwrite("./static/result/{}".format(filename), img)


    labels=[ i for i in label_map ]
    eq=[]
    pos=[]
    for i in ((chars)):
        if len(eq)==0 and i[0][0] in labels[3:]:
            eq.append(i[0][0])
            print(f"첫번째 loop i : {i[0][0]}, eq = {eq[0]}" )
        elif len(eq)>0 and i[0][0] in labels[4:14]:
            eq.append(i[0][0])
            print(f"두번째 loop i : {i[0][0]}, eq = {eq[0]}")
    
        elif len(eq)>0 and i[0][0] in labels[:4]:
            eq.append(i[0][0])
            pos.append(len(eq))
            print(f"세번째 loop i : {i[0][0]}, eq = {eq[0]}, pos = {pos}")
        else:
            pass

    for i in pos:
        if eq[i-1]=='+':
            sol = int(''.join(eq[:pos[0]-1]))+int(''.join(eq[pos[0]:]))
        elif eq[i-1]=='%': 
            sol = int(''.join(eq[:pos[0]-1]))/int(''.join(eq[pos[0]:]))
        elif eq[i-1]=='*':
            sol = int(''.join(eq[:pos[0]-1]))*int(''.join(eq[pos[0]:]))
        else:
            sol = int(''.join(eq[:pos[0]-1]))-int(''.join(eq[pos[0]:]))
    return sol