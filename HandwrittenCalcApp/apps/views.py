##############
## views.py ## 
##############
from flask import render_template, request
from PIL import Image
from tensorflow.python.framework.ops import Operation
from apps import utils

def index():
    return render_template("index.html")


def calcapp():
    return render_template("calcapp.html")


def calculation():
    if request.method == "POST":
        # POST 형식으로 input file을 받는다.
        f = request.files["image"]
        filename = f.filename
        path = "./static/uploads/" + filename
        f.save(path)
        w = getwidth(path)
        sol, rightSide, leftSide, operator = utils.pipeline_model(path, filename, color="bgr")  # 예측 값

        return render_template("calculation.html", fileupload=True, img_name=filename, w=w, sol=sol, rightSide=rightSide, leftSide=leftSide, operator=operator)

    return render_template("calculation.html", fileupload=False, img_name="")


def getwidth(path):
    img = Image.open(path)
    size = img.size # width and height
    aspect = size[0] / size[1] # width / height
    w = 300 * aspect
    return int(w)