from flask import Flask,request
import tensorflow as tf
import numpy as np
from skimage import transform
from PIL import Image
import PIL.ImageOps
import base64
from io import BytesIO

app = Flask(__name__)
model = tf.keras.models.load_model('model_2.h5')

@app.route('/test', methods=['POST','GET']) 
def foo():
    data = request.data
    imgdata = base64.b64decode(data)
    stream = BytesIO(imgdata)
    def load(filename):
        np_image = Image.open(filename)
        np_image.save("test22.png")
        # np_image.save("test.jpg", "JPEG", quality=100, optimize=True, progressive=True)
        np_image = np.array(np_image).astype('float32')/255
        np_image = transform.resize(np_image, (28, 28, 1))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image
        
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

    img = load("predict.png")
    result = model.predict(img)

    predict_classes = np.argmax(result ,axis=1)

    print("result = ", result)
    print("test = ", predict_classes[0])
    print("print = ", predict_classes)

    return str(predict_classes[0])

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='8000', debug=True)