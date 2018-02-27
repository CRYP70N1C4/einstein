import numpy as np
import random,re
from PIL import Image

char_set=['7', 'p', 'w', 'n', '3', 'd', '6', 'b', '4', '2', 'g', 'a', 'c', '8', 'f', 'x', 'e', 'y', '5', 'm']
width, height, n_len, n_class = 100, 35, 6, len(char_set)


def text2vec(text):
    text_len = len(text)
    if text_len > n_len:
        raise ValueError('验证码最长6个字符')

    vector = np.zeros(n_len * n_class)

    for i, c in enumerate(text):
        idx = i * n_class + char_set.index(c)
        vector[idx] = 1
    return vector

content=None
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
    image=Image.open(img_path,"r")
    image.thumbnail((width,height), Image.ANTIALIAS)
    captcha_image = np.array(image)
    captcha_text = re.search('.*([a-z0-9]{6})\\.png', img_path).group(1)
    return captcha_text, captcha_image


def get_next_batch(batch_size=128):
    """
    # 生成一个训练batch
    :param batch_size:
    :return:
    """
    batch_x = np.zeros([batch_size, height * width])
    batch_y = np.zeros([batch_size, n_len * n_class])

    for i in range(batch_size):
        text, image = gen_captcha_text_and_image()
        batch_x[i, :] = np.mean(image, -1).flatten() / 255  # (image.flatten()-128)/128  mean为0
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y