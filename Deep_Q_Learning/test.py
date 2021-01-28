import tensorflow as tf
import numpy as np
import os

try:
    sub_dir = 'models\\'
    model_file = os.listdir(sub_dir)
    model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[1])
    print('models\\'+os.listdir('models\\')[0])
    # model = tf.keras.models.load_model(sub_dir + model_file[0])
    print('model ready')
except:
    print('No model to load.')
