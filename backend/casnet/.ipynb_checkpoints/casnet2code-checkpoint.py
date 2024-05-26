#!/usr/bin/env python
# coding: utf-8

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import *
from tensorflow.keras.preprocessing import image as kpi
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras import losses
import matplotlib.pyplot as plt
from PIL import Image

# Ensure TensorFlow uses GPU if available
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Function to get image data
def get_image_data(img_path, image_size, space='rgb'):
    if space == 'rgb':
        img = kpi.load_img(img_path, target_size=image_size)
        x = kpi.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        data = x[0]
    elif space == 'gray':
        img = kpi.load_img(img_path, target_size=image_size, color_mode='grayscale')
        x = kpi.img_to_array(img)
        x /= 255.
        data = x
    elif space == 'hsv':
        imc = cv2.imread(img_path)
        imc = cv2.resize(imc, (image_size[1], image_size[0]))
        hsv = cv2.cvtColor(imc, cv2.COLOR_BGR2HSV)
        data = hsv
    return data

# Function to create model
def create_dilate_vgg16_model(with_sigmoid=False, with_centerbias=False, with_aspp_pointwise=True, aspp_sizes=None, with_aspp_pooling=False):
    model_file = os.path.expanduser('~') + '/.keras/models/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'
    
    input_x = Input(shape=(480, 640, 3))
    # VGG16 conv layers
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(input_x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool', padding='same')(x)
    
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool', padding='same')(x)
    
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool', padding='same')(x)
    
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool', padding='same')(x)
    
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1', dilation_rate=(1, 1))(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2', dilation_rate=(2, 2))(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3', dilation_rate=(3, 3))(x)
    
    dilate_vgg16_model = Model(inputs=input_x, outputs=x)
    dilate_vgg16_model.load_weights(model_file)
    
    aspp_list = []
    if with_aspp_pointwise:
        aspp_list.append(Conv2D(512, (1, 1), activation='relu', padding='same', name='block_aspp_point_wise')(x))
    
    if aspp_sizes:
        for ind, aspp_size in enumerate(aspp_sizes):
            aspp_list.append(Conv2D(512, (3, 3), activation='relu', padding='same', name=f'block_aspp_conv{ind}', dilation_rate=(aspp_size, aspp_size))(x))
    
    if with_aspp_pooling:
        aspp_list.append(MaxPooling2D((2, 2), strides=(1, 1), padding='same', name='block_aspp_maxpooling')(x))
    
    if aspp_list:
        o = Concatenate()(aspp_list)
    else:
        o = dilate_vgg16_model.get_layer('block5_conv3').output
        
    o = Conv2D(512 * len(aspp_list), (1, 1), activation='relu')(o)
    o = Conv2D(1024, (1, 1), activation='relu')(o)
    
    o = Lambda(lambda x: x / 255., name='lambda_norm')(o)
    w_o = MaxPooling2D(pool_size=(4, 4))(o)
    w_o = Flatten()(w_o)
    w_o = Dense(1024)(w_o)
    o = Multiply()([o, w_o])
    o = Conv2D(1, (1, 1), name='weighted_sum')(o)
    
    model = Model(inputs=input_x, outputs=o)
    return model

def NSS(y_true, y_pred):
    epsilon = 1e-7
    fix_pts = tf.where(tf.equal(y_true, tf.reduce_max(y_true)))
    std = tf.sqrt(tf.reduce_mean(tf.square(y_pred - tf.reduce_mean(y_pred))))
    mean = tf.reduce_mean(y_pred)
    y_pred_norm = (y_pred - mean) / (std + epsilon)
    return tf.reduce_mean(tf.gather_nd(y_pred_norm, fix_pts))

def Multi_Loss(y_true, y_pred):
    return 10. * losses.mse(y_true, y_pred) + (1. - tf.sigmoid(NSS(y_true, y_pred)))

# Main execution
if __name__ == "__main__":
    # Load the model
    model = create_dilate_vgg16_model(with_sigmoid=False, 
                                      with_centerbias=False, 
                                      with_aspp_pointwise=True,
                                      aspp_sizes=[3, 6, 9], 
                                      with_aspp_pooling=False)
    model.compile(loss=Multi_Loss, optimizer="sgd", metrics=[])
     
    # Load pre-trained weights
    MODEL_NAME = 'C:/Pedro/ISEP/PESTI/backend/casnet/vgg16_S17_dialate_ASPPv3_pooling_25_epoch_30.h5'
    model = load_model(MODEL_NAME, custom_objects={"Multi_Loss": Multi_Loss})
    
    # Get the image path from command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    img_path = sys.argv[1]
    original_img = Image.open(img_path)
    
    x1 = np.expand_dims(get_image_data(img_path, (480, 640), space="rgb"), axis=0)
    x2 = np.expand_dims(get_image_data(img_path, (300, 400), space="rgb"), axis=0)
    res = model.predict([x1, x2])
    sal = Image.fromarray(np.uint8(res[0, :, :, 0] * 255), mode='L').resize(original_img.size, Image.BICUBIC)

    # Blend the saliency map with the original image
    combined_img = Image.new('RGB', original_img.size)
    combined_img.paste(original_img, (0, 0))
    combined_img.paste(sal.convert('RGB'), (0, 0), sal)


    plt.imshow(sal)
    save_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/temp.jpg'
    plt.savefig(save_path)

