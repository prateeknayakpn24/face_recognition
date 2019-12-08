from typing import List,Any

import pandas as pd
import cv2
import os
from PIL import Image
import numpy as np
import pickle
from sklearn.svm import SVC

x_train = []
y_label = []
label_ids = {}
ids = []

base_dir = os.getcwd()
image_dir = os.path.join(base_dir,'images')

recognizer = cv2.face.LBPHFaceRecognizer_create()

for root,dirs,files in os.walk(image_dir):
    for file in files:
        if file.endswith('jpg') or file.endswith('png'):
            path = os.path.join(root,file)
            label = os.path.basename(root)
            name_id=label.split('_')
            name = name_id[0]
            id = name_id[1]
            #y_label.append(id)
            if not name in label_ids or not id in ids:
                label_ids[id]=name
                y_label.append(id)
            pil_image = Image.open(path)
            image_array = np.array(pil_image,'uint8')
            x_train.append(image_array)


y_label = list(map(int, y_label))
df=pd.DataFrame(y_label)
y_label=df.iloc[:,:].values

with open('names.pickle','wb') as f:
    pickle.dump(label_ids,f)
print('Training...')
recognizer.train(x_train,y_label)
recognizer.save('trainer.yml')
print('Training Completed')