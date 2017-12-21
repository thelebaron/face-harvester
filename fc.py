import sys 
import os
import glob
import shutil
import cv2
import face_recognition
import numpy
import argparse
from contextlib import contextmanager
from PIL import Image

sys.path.append('/usr/local/lib/python2.7/site-packages')

# this is a percentage
FACEPADDING = 1.20

SCRIPTPATH = os.getcwd()
DIRECTORYS = "training_image_src"
DIRECTORY0 = "training_image_backup"
DIRECTORY1 = "training_image_crops"
#update working paths, the "" is a slash
PATHS = os.path.join(SCRIPTPATH, '', DIRECTORYS)
PATH0 = os.path.join(SCRIPTPATH, '', DIRECTORY0)
PATH1 = os.path.join(SCRIPTPATH, '', DIRECTORY1)

INPUT_FILETYPES = ['*.jpg', '*.jpeg', '*.bmp', '*.dib', '*.jp2',
                   '*.png', '*.webp', '*.pbm', '*.pgm', '*.ppm',
                   '*.sr', '*.ras', '*.tiff', '*.tif']
FILES_GRABBED = []

def setup():
    print("Setting up")

    if os.path.isdir(DIRECTORYS):
        print("Directory exists " + str(DIRECTORYS))
    else:
        print("Directory doesnt exist! Will exit after making " + str(DIRECTORYS) + " please remember to drop your source files there.")
        os.makedirs(DIRECTORYS)
    if os.path.isdir(DIRECTORY0):
        print("Directory exists " + str(DIRECTORY0))
    else:
        print("Directory doesnt exist, making " + str(DIRECTORY0))
        os.makedirs(DIRECTORY0)

    if os.path.isdir(DIRECTORY1):
        print("Directory exists " + str(DIRECTORY1))
    else:
        print("Directory doesnt exist, making " + str(DIRECTORY1))
        os.makedirs(DIRECTORY1)

    #change to source path with our images
    os.chdir(PATHS)

setup()

def crop():
    print("Crop Def")

def main(fheight, fwidth):
    print("Main Def")

main("256","256")


for files in INPUT_FILETYPES:
    FILES_GRABBED.extend(glob.glob(files))

for file in FILES_GRABBED:
    # Copy to /backup dir
    shutil.copy(file, str(PATH0))

    ##CV2 stuff to get image size > planned head to image ratio > make offsets
    img = cv2.imread(file)
    img_height, img_width, channels = img.shape
    print(str(img_height))
    print(str(img_width))


    # loads into an array
    image = face_recognition.load_image_file(file)

    # actual face detection
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
    print(str(file) + "I found {} face(s) in this photograph.".format(len(face_locations)))



    #https://github.com/ageitgey/face_recognition/blob/master/examples/find_facial_features_in_picture.py
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

    for face_landmarks in face_landmarks_list:
        # Print the location of each facial feature in this image
        facial_features = [
            'chin',
            'left_eyebrow',
            'right_eyebrow',
            'nose_bridge',
            'nose_tip',
            'left_eye',
            'right_eye',
            'top_lip',
            'bottom_lip'
        ]

        print(str(len(face_landmarks_list))) #expected 9 got 1??
        print (str(len(face_landmarks['left_eye']))) #expected and got 6
        print(str(face_landmarks['left_eye'])) #prints all the coords

        #print(str(face_landmarks['left_eye',[1,3]]))
        z = [c[0] for c in face_landmarks['left_eye'] ]
        print("z " + str(z))

        #finally gets coordinates
        for a, b in face_landmarks['left_eye']:   # <-- this unpacks the tuple like a, b = (0, 1)
            print(a, b)
            print(a)
            

        #for landmark in face_landmarks['left_eye']:
            #print("Eyessss {} has {}".format(facial_features['left_eye'], face_landmarks['left_eye']))

        
        for facial_feature in facial_features:
            #print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
            print("Eye {} has {}".format(facial_feature, face_landmarks['left_eye']))
            print("space")
            print("Eye has {}".format(face_landmarks['left_eye']))






    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))


        ##GET DIMENSIONS
        face_width = right - left
        face_height = bottom - top
        offsetWidthNeeded = False
        offsetHeightNeeded = False
        diff = 0
        #Find longest edge so we can make a square
        if(face_height > face_width):
            diff = face_height - face_width
            offsetWidthNeeded = True
        if(face_width > face_height):
            diff = face_width - face_height
            offsetHeightNeeded = True

        #hmm does this work?
        if(offsetWidthNeeded):
            face_width = face_height
        if(offsetHeightNeeded):
            face_height = face_width


        #pad it so we dont crop too close
        face_width_padded = face_width * FACEPADDING
        #print("face height padded is "+ str(face_width_padded))
        face_height_padded = face_height * FACEPADDING
        pix_width = face_width_padded - face_width
        pix_height = face_height_padded - face_height
        #print("pix_width is "+ str(pix_width))

        pix_width_pad_amt = pix_width * 2
        pix_height_pad_amt = pix_height * 2
        #print("pix_width is "+ str(pix_width_pad_amt))

        #offset with actual padding amount in pixels
        top -= int(pix_height_pad_amt)
        if top < 0:
            top = 0
        bottom += int(pix_height_pad_amt)
        if bottom > img_height:
            bottom = img_height
        left -= int(pix_width_pad_amt)
        if left < 0:
            left = 0
        right += int(pix_width_pad_amt)
        if right > img_width:
            right = img_width


        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        #pil_image.show()
        
        pil_image = pil_image.resize((256,256), Image.ANTIALIAS)
        # Write cropfile
        cropfilename = '{0}'.format(str(file))
        #cv2.imwrite(cropfilename, face_image)
        pil_image.save(cropfilename, "JPEG")
        # Move files to /crop
        shutil.copy(cropfilename, str(PATH1))
        os.remove(cropfilename)




"""
# Load the jpg file into a numpy array
image = face_recognition.load_image_file("test2.jpg")

# Find all the faces in the image using a pre-trained convolutional neural network.
# This method is more accurate than the default HOG model, but it's slower
# unless you have an nvidia GPU and dlib compiled with CUDA extensions. But if you do,
# this will use GPU acceleration and perform well.
# See also: find_faces_in_picture.py
face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    sys.exit()
    


#pil_image.show()
"""

