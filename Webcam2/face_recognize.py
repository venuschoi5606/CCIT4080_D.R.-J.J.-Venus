# facerec.py
import cv2, sys, numpy, os
from pyfirmata import Arduino
import time

# Reference: https://github.com/vschs007/flask-realtime-face-detection-opencv-python

################ Arduino ##############
# Edit COM number when connected to Arduino
board = Arduino('COM6')

# initializing the LEDs
ledB = board.get_pin('d:13:o') #B
ledG = board.get_pin('d:12:o') #G
ledY = board.get_pin('d:11:o') #Y
ledR = board.get_pin('d:10:o') #R
wait = 1

val_1 = val_2 = val_3 = val_4 = False
ledB.write(val_1)
ledG.write(val_2)
ledY.write(val_3)
ledR.write(val_4)
################ Arduino ##############

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
# Part 1: Create fisherRecognizer
print('Recognizing Face Please Be in sufficient Light Conditions...')
# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, lables)

# Part 2: Use fisherRecognizer on camera stream
face_cascade = cv2.CascadeClassifier(haar_file)
# IMPORANT: maybe need to change from 0 to 1 for USB Camera
webcam = cv2.VideoCapture(1)

while True:
    ledG.write(False)
    ledR.write(True)
    print("Door Closed")
    positive_count = 0
    while True:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            prediction = model.predict(face_resize)

            if prediction[1]<80: # threshold, the lager the prediction value, the less similar the figure
                cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                positive_count+=1;
                print(positive_count)
            else:
                cv2.putText(im,'not recognized %.0f' % (prediction[1]) ,(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 0, 255))
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
                positive_count=0;
                print(positive_count)

        cv2.imshow('OpenCV', im)

        if positive_count > 5:
            ledG.write(True)
            ledR.write(False)
            print("Door Open")
            time.sleep(10)
            break

        # press 'esc' to escape
        key = cv2.waitKey(1000)
        if key == 27:
             break
    if key == 27:
        break
