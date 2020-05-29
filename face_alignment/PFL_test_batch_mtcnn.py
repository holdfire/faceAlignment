# Face alignment demo
# Uses MTCNN as face detector
# Cunjian Chen (ccunjian@gmail.com)
from __future__ import division
import argparse
import torch
import os
import cv2
import numpy as np
#import dlib
from common.utils import BBox,drawLandmark,drawLandmark_multiple
from models.basenet import MobileNet_GDConv
import matplotlib.pyplot as plt
from src import detect_faces
import glob
import time
parser = argparse.ArgumentParser(description='PyTorch face landmark')
# Datasets
parser.add_argument('-img', '--raptor_result', default='face76', type=str)
parser.add_argument('-j', '--workers', default=8, type=int, metavar='N',
                    help='number of data loading workers (default: 4)')
parser.add_argument('--gpu_id', default='0,1', type=str,
                    help='id(s) for CUDA_VISIBLE_DEVICES')
parser.add_argument('-c', '--checkpoint', default='checkpoint/mobilenet_224_model_best_gdconv.pth.tar', type=str, metavar='PATH',
                    help='path to save checkpoint (default: checkpoint)')

args = parser.parse_args()
mean = np.asarray([ 0.485, 0.456, 0.406 ])
std = np.asarray([ 0.229, 0.224, 0.225 ])

if torch.cuda.is_available():
    map_location=lambda storage, loc: storage.cuda()
else:
    map_location='cpu'

def load_model():
    model = MobileNet_GDConv(136)
    #model = torch.nn.DataParallel(model)
    checkpoint = torch.load(args.checkpoint, map_location=map_location)
    model.load_state_dict(checkpoint['state_dict'])
    return model

if __name__ == '__main__':
    print("current work directory:", os.getcwd())
    out_size = 224
    model = load_model()
    model = model.eval()
    filenames=glob.glob("samples/14--Group/*.[jp][pn]g")
    for imgname in filenames:
        print(imgname)
        img = cv2.imread(imgname)
        height,width,_=img.shape
        # perform face detection using MTCNN
        from PIL import Image
        image = Image.open(imgname)
        faces, landmarks = detect_faces(image)
        print("mtcnn results faces:", faces)
        print("mtcnn results landmarks:", landmarks)
        ratio=0
        if len(faces)==0:
            print('NO face is detected!')
            continue
        for k, face in enumerate(faces): 
            x1=face[0]
            y1=face[1]
            x2=face[2]
            y2=face[3]
            w = x2 - x1 + 1
            h = y2 - y1 + 1
            size = int(min([w, h])*1.2)
            cx = x1 + w//2
            cy = y1 + h//2
            x1 = cx - size//2
            x2 = x1 + size
            y1 = cy - size//2
            y2 = y1 + size

            dx = max(0, -x1)
            dy = max(0, -y1)
            x1 = max(0, x1)
            y1 = max(0, y1)

            edx = max(0, x2 - width)
            edy = max(0, y2 - height)
            x2 = min(width, x2)
            y2 = min(height, y2)
            new_bboxx = list(map(int, [x1, x2, y1, y2]))
            # save the croped face
            np.savetxt(os.path.join('result_mine/rect', os.path.basename(imgname)+"_cropped_"+str(k+1)+".rect"), new_bboxx, delimiter=" ")
            new_bbox = BBox(new_bboxx)
            cropped=img[new_bbox.top:new_bbox.bottom,new_bbox.left:new_bbox.right]
            cv2.imwrite(os.path.join('result_mine/picture_crop', os.path.basename(imgname)+"_cropped_"+str(k+1)+".jpg"), cropped)
            if (dx > 0 or dy > 0 or edx > 0 or edy > 0):
                cropped = cv2.copyMakeBorder(cropped, int(dy), int(edy), int(dx), int(edx), cv2.BORDER_CONSTANT, 0)            
            cropped_face = cv2.resize(cropped, (224, 224))

            if cropped_face.shape[0]<=0 or cropped_face.shape[1]<=0:
                continue
            test_face = cv2.resize(cropped_face,(224,224))
            test_face = test_face/255.0
            test_face = (test_face-mean)/std
            test_face = test_face.transpose((2, 0, 1))
            test_face = test_face.reshape((1,) + test_face.shape)
            input = torch.from_numpy(test_face).float()
            input= torch.autograd.Variable(input)
            start = time.time()
            landmark = model(input).cpu().data.numpy()
            end = time.time()
            print('Time: {:.6f}s.'.format(end - start))
            landmark = landmark.reshape(-1,2)
            landmark = new_bbox.reprojectLandmark(landmark)
            # sace thelandmarks
            np.savetxt(os.path.join('result_mine/landmark', os.path.basename(imgname)+"_cropped_"+str(k+1)+".txt"), landmark)
            img = drawLandmark_multiple(img, new_bbox, landmark)
            print(img.shape)
            #img_crop = np.array((new_bboxx[1]+1-new_bboxx[0], new_bboxx[3]+1-new_bboxx[2], 3))
            print(new_bboxx)
            img_crop = img[new_bboxx[2]:new_bboxx[3]+1, new_bboxx[0]:new_bboxx[1]+1,:]
            print(img_crop.shape)
            cv2.imwrite(os.path.join('result_mine/crop_landmark', os.path.basename(imgname)+"_cropped_landmark_"+str(k+1)+".jpg"), img_crop)
        print(imgname)
        cv2.imwrite(os.path.join('result_mine/draw_landmark',os.path.basename(imgname)+"_draw_rect_landmark.jpg"),img)

