from keras.models import *
from keras.layers import *
import numpy as np
import random,re
from PIL import Image

char_set=['7', 'p', 'w', 'n', '3', 'd', '6', 'b', '4', '2', 'g', 'a', 'c', '8', 'f', 'x', 'e', 'y', '5', 'm']
width, height, n_len, n_class = 200, 70, 6, len(char_set)
# 图像大小
IMAGE_HEIGHT = 70
IMAGE_WIDTH = 200
MAX_CAPTCHA = 6
CHAR_SET_LEN = n_class

content = None
def text2vec(text):
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        raise ValueError('验证码最长6个字符')

    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)

    for i, c in enumerate(text):
        idx = i * CHAR_SET_LEN + char_set.index(c)
        vector[idx] = 1
    return vector


def gen_captcha_text_and_image():
    """
    生成字符对应的验证码
    :return:
    """
    global content
    if not content:
        with open("E:\Repository\captcha\dataset1.log") as f:
            content = [line.rstrip('\n') for line in f]
    img_path=random.sample(content,1)[0]
    captcha_image = np.array(Image.open(img_path,"r"))
    captcha_text = re.search('.*([a-z0-9]{6})\\.png', img_path).group(1)
    return captcha_text, captcha_image

def gen(batch_size=32):
    X = np.zeros((batch_size, height, width, 3), dtype=np.uint8)
    y = np.zeros((batch_size, n_class*MAX_CAPTCHA), dtype=np.uint8)
    while True:
        for i in range(batch_size):
            text, image = gen_captcha_text_and_image()
            X[i] = image
            y[i] = text2vec(text)
        yield X, y

def get_next_batch(batch_size=128):
    """
    # 生成一个训练batch
    :param batch_size:
    :return:
    """
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])

    for i in range(batch_size):
        text, image = gen_captcha_text_and_image()
        batch_x[i, :] = np.mean(image, -1).flatten() / 255  # (image.flatten()-128)/128  mean为0
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y

# Build the neural network!
def setup_model():
    input_tensor = Input((height, width, 3))
    x = input_tensor
    for i in range(4):
        x = Convolution2D(32 * 2 ** i, 3, 3, activation='relu')(x)
        x = Convolution2D(32 * 2 ** i, 3, 3, activation='relu')(x)
        x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)
    x = Dropout(0.25)(x)
    x = [Dense(n_class, activation='softmax', name='c%d' % (i + 1))(x) for i in range(6)]
    model = Model(input=input_tensor, output=x)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    return model;


import sys
if __name__ == '__main__':
    model = setup_model()
    model.fit_generator(gen(), samples_per_epoch=51200, nb_epoch=5,
                        nb_worker=2, pickle_safe=True,
                        validation_data=gen(), nb_val_samples=1280)
    model.save("E:\\Repository\\github\\einstein\\model\\model1",overwrite=True)
