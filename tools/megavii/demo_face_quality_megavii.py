import os
import glob
import sys
import cv2

from demo_detect_api import *

path_img_list = '/ssd/cxzhao/data/quality_badcase/ctf_badcase/bbox_list.txt'
path_out_list = '/ssd/cxzhao/data/quality_badcase/ctf_badcase/bbox_list_res_megavii.txt'

path_tmp = '/ssd/cxzhao/data/quality_badcase/ctf_badcase/tmp'
path_img = path_tmp + '/imgs'
os.makedirs(path_img, exist_ok=True)
path_json = path_tmp + '/json_530'
os.makedirs(path_json, exist_ok=True)
path_json_pairs_list = path_tmp + '/list_json_pairs.txt'

def get_face_box(bbox, img_shape, scale = 2.0):
    x, y, w, h = bbox
    img_h, img_w = img_shape[:2]
    x_mid = (2*x+w)/2
    y_mid = (2*y+h)/2
    sw = w * scale / 2
    sh = h * scale / 2
    x_min = int( max(0, x_mid - sw) )
    x_max = int( min(img_w, x_mid + sw) )
    y_min = int( max(0, y_mid - sh) )
    y_max = int( min(img_h, y_mid + sh) )
    return [x_min, y_min, x_max, y_max]

def process_line(line):
    img_path, x, y, w, h, conf = line.strip().split()
    
    img_name = os.path.split(img_path)[-1]
    save_path = os.path.join(path_img, img_name)
    json_path = os.path.join(path_json, img_name[:-4] + '.txt')

    left = int(float(x))
    top = int(float(y))
    w = int(float(w))
    h = int(float(h))
    bbox = [left, top, w, h]

    img = cv2.imread(img_path)
    x_min, y_min, x_max, y_max = get_face_box(bbox, img.shape, scale = 1.5)
    face = img[y_min:y_max, x_min:x_max, :]

    cv2.imwrite(save_path, face)

    get_attributes_json(save_path, json_path) 
    quality = decode_face_quality_from_attributes_json(json_path)    

    line_res = img_path + ' ' + str(quality) + '\n'
    return line_res

def process():
    with open(path_img_list, 'r') as fid:
        lines = fid.readlines()
    lines_res = []
    for l, line in enumerate(lines):
        if l>10:
            break
        line_new = process_line(line)
        lines_res.append(line_new)
    
    with open(path_out_list, 'w') as fid:
        fid.writelines(lines_res)

if __name__ == '__main__':
    process()






