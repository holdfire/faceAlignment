import os
import glob
import json
import cv2

path_txt = '/ssd/cxzhao/code/scripts/quality/quality_data_self_label_v1/txt/all_data_list_pairs.txt'
path_save = '/ssd/cxzhao/code/scripts/quality/quality_data_self_label_v1/txt/all_data_list_quality.txt'

def norm_quality(quality):
    return quality / 100.0

def get_quality(img_path, json_path):
    img_name = os.path.split(img_path)[-1]
    
    if not os.path.exists(json_path):
        print('No json_530:', img_path)
        return ''

    with open(json_path, 'r') as fid:
        line = fid.readlines()[0]
    line = line.replace('\'', '\"')
    #print(line)
    face_info = json.loads(line.strip())
    
    if not 'faces' in face_info.keys():
        print('No key faces', img_path, line)
        return ''

    if face_info['faces'] == []:
        print('No faces', img_path, line)
        face_quality = 0.0
        line_new = img_path + ' ' + str(face_quality) + '\n'
        return line_new    
    bbox_info = face_info['faces'][0]['face_rectangle']
    left, top, width, height = bbox_info['left'], bbox_info['top'], bbox_info['width'], bbox_info['height']
    face_quality = face_info['faces'][0]['attributes']['facequality']['value']
    face_quality = norm_quality(face_quality)

    line_new = img_path + ' ' + str(face_quality) + '\n'
    print(img_path, face_quality)
    #save_path = os.path.join(path_save, img_name[:-4] + '_%.5f.jpg'%(face_quality))
    #face = img[top:top+height, left:left+width, :]
    #cv2.imwrite(save_path, face)
    return line_new

def process():
    with open(path_txt, 'r') as fid:
        lines = fid.readlines()
    lines_res = []
    for l, line in enumerate(lines):
        print('line:', l)
        name_splits = line.strip().split()
        if not len(name_splits) == 2:
            continue
        img_path, json_path = name_splits[:2]
        line_new = get_quality(img_path, json_path)
        lines_res.append(line_new)

    with open(path_save, 'w') as fid:
        fid.writelines(lines_res)

if __name__ == '__main__':
    process()
