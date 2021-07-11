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
## faceapp == calcapp , detection == calculation

def calculation():
    if request.method == "POST":
        f = request.files["image"]
        filename = f.filename
        path = "./static/uploads/" + filename
        f.save(path)
        w = getwidth(path)
        sol, rightSide, leftSide, operator = utils.pipeline_model(path, filename, color="bgr")

        return render_template("calculation.html", fileupload=True, img_name=filename, w=w, sol=sol, rightSide=rightSide, leftSide=leftSide, operator=operator)

    return render_template("calculation.html", fileupload=False, img_name="")

def getwidth(path):
    img = Image.open(path)
    size = img.size # width and height
    aspect = size[0] / size[1] # width / height
    w = 300 * aspect
    return int(w)