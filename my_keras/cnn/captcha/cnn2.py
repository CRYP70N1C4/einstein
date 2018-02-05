from keras.models import  *
from keras.layers import *

def captcha_model():
    width, height, n_len, n_class = 170,80,6,36
    input_tensor = Input(shape=(3,height,width))
    x = input_tensor
    for i in range(4):
        x = Convolution2D(32*2**i,3,3,activation='relu')(x)
        x = Convolution2D(32*2**i,3,3,activation='relu')(x)
        x = BatchNormalization(axis=1)(x)
        x = MaxPooling2D((2,2))(x)
    x = Flatten()(x)
    x = [Dense(n_class,activation='softmax',name='c%d' % (i+1))(x) for i in range(n_len)]
    model = Model(input=input_tensor,output=x)
    return model

if __name__ == '__main__':
    print(captcha_model())