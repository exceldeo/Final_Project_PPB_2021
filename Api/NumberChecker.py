
import io
import tensorflow as tf
import numpy as np
from skimage import transform
from PIL import Image
import PIL.ImageOps
import base64

model = tf.keras.models.load_model('model_2.h5')

base = '''iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABx0lEQVR4nG2STUhUURTHf+fcq2NjizYSzICrNApCLAgzqMRAamjnKiLa1C7aJLRrEQRuohaCLUKjZS0CaVNELkowkHCkaNDBDCaSBFGnZvJ93BZvHvPe2Fmdcw+/8/G/R2iaiAgEjv+Y7nmRpuNs7/CRXe5tulZWhP4nH51z7iSmhRTH5TsHK1/VO9o1Md7mpTjNji9VnnUDt13tQpONZhnbKl4CNbbz4fdXZ5LDKceK6zcwCoLc3XjZJZJIXl95hBEAlY7n5dGosAKEXMuXjTiA0NYrudHU5qu6LxCjqqqwG3i4RNmrpffn4ygzVyxEkAVw8m7o4tTjudUQZ2q3+n8W0yLmJ9c3f+9Uq1u15fLKzbTOluPOc5F9KsQ5G5FhZuRPtlQVlE7fpmVXhhZ/TGYB2q+sLQ8k9RNyM6UxEBB46k20J3oaCkuzogpgpG9+/lTUVSOy95AlDAECXXzbfTalkLHqGq7o9oERwua0VOvaUTcIYPyN7S+Iawr/ZjY3dSIIfN/3/7ad9hfidgDqBh/07LywRgR6Bmbuf5Ywuczh12u/IoX8D30NJv5xDffnzw2raJBZmP4mLce596QTR41II3DE/f4B2T6hMxOd2PYAAAAASUVORK5CYII='''


imgdata = base64.b64decode(base)
stream = io.BytesIO(imgdata)
def load(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (28, 28, 1))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image
img = load(stream)
result = model.predict(img)
predict_classes = np.argmax(result ,axis=1)
print(predict_classes)




