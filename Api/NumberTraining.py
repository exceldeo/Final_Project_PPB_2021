#!/usr/bin/env python
# coding: utf-8

# In[25]:


import tensorflow as tf


def solution_C2():
    mnist = tf.keras.datasets.mnist

    # YOUR CODE HERE
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # YOUR CODE HERE

    #Normalization
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(
        x_train,
        y_train,
        validation_data=(x_test, y_test),
        epochs = 20,
        verbose = 1)
    return model


# The code below is to save your model as a .h5 file.
# It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    if __name__ == '__main__':
        model = solution_C2()
        model.save("model_2a.h5")


# In[7]:


import tensorflow as tf
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
from skimage import transform


# In[19]:


img = cv2.imread('./test2.png')
plt.imshow(img , cmap='gray')


# In[20]:


def load(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (28, 28, 1))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image


# In[21]:


model = tf.keras.models.load_model('model_C2.h5')


# In[22]:


img = load('./test2.png')


# In[23]:


result = model.predict(img)
predict_classes = np.argmax(result ,axis=1)


# In[24]:


predict_classes


# In[ ]:





# In[ ]:


results = model.predict(img)


# In[ ]:




