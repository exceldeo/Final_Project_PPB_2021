from flask import Flask,request
from PIL import Image
import PIL.ImageOps
import base64
from io import BytesIO
import sys
import pickle
import matplotlib.pyplot as plt
import PIL

app = Flask(__name__)

@app.route('/test', methods=['POST','GET']) 
def foo():
    data = request.data
    imgdata = base64.b64decode(data)
    stream = BytesIO(imgdata)

    basewidth = 28
    img = Image.open(stream)

    img_w, img_h = img.size
    size = max(img_w, img_h) + 50
    background = Image.new('RGBA', (size, size), (0, 0, 0, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    img = background
    img.save("predict1.png")

    img = img.resize((basewidth,basewidth),PIL.Image.ANTIALIAS)
    img = img.convert('L')
    img.save("predict.png")

    data = plt.imread("predict.png")

    f = open('LogisticRegressionDigit.pkl', 'rb')
    model = pickle.load(f)

    dataImg = data.reshape(1, 784)
    print(model.predict(dataImg)[0])

    return str(model.predict(dataImg)[0])

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='8000', debug=True)