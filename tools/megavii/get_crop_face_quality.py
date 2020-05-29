import os
import glob
import json
import cv2

path_txt = '/ssd/cxzhao/data/quality_badcase/hf_sq/test_list_json_pairs.txt'
path_save = '/ssd/cxzhao/data/quality_badcase/hf_sq/res_megavii'
os.makedirs(path_save, exist_ok=True)

def get_crop(img_path, json_path):
    img_name = os.path.split(img_path)[-1]
    
    img = cv2.imread(img_path)
    with open(json_path, 'r') as fid:
        line = fid.readlines()[0]
    line = line.replace('\'', '\"')
    print(line)
    face_info = json.loads(line.strip())
    
    if face_info['faces'] == []:
        save_path = os.path.join(path_save, img_name[:-4] + '_%.5f.jpg'%(-1.0))
        cv2.imwrite(save_path, img)
        return 0    
    bbox_info = face_info['faces'][0]['face_rectangle']
    left, top, width, height = bbox_info['left'], bbox_info['top'], bbox_info['width'], bbox_info['height']
    face_quality = face_info['faces'][0]['attributes']['facequality']['value']
    
    save_path = os.path.join(path_save, img_name[:-4] + '_%.5f.jpg'%(face_quality))
    face = img[top:top+height, left:left+width, :]
    cv2.imwrite(save_path, face)
    return 1

def process():
    with open(path_txt, 'r') as fid:
        lines = fid.readlines()
    for l, line in enumerate(lines):
        img_path, json_path = line.strip().split()
        img = get_crop(img_path, json_path)

if __name__ == '__main__':
    process()
