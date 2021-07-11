from flask import Flask
from apps import views

app = Flask(__name__)

app.add_url_rule("/", "index", views.index)
app.add_url_rule("/calcapp", "calcapp", views.calcapp)
app.add_url_rule("/faceapp/calculaion", "calculation", views.calculation, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(debug=True)
    
