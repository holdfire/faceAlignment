import os
import glob

path_data = '/ssd/cxzhao/data/quality_badcase/hf_sq/imgs'
path_json = '/ssd/cxzhao/data/quality_badcase/hf_sq/json_530'
os.makedirs(path_json, exist_ok=True)

path_txt = '/ssd/cxzhao/data/quality_badcase/hf_sq/test_list_json_pairs.txt'

def process():
    IMAGES = glob.glob(os.path.join(path_data, '*/*.jpg'))
    lines = []
    for k, img_path in enumerate(IMAGES):
        img_name = os.path.split(img_path)[-1]
        json_path = os.path.join(path_json, img_name[:-4] + '.txt')
        lines.append(img_path + ' ' + json_path + '\n')
    with open(path_txt, 'w') as fid:
        fid.writelines(lines)

if __name__ == '__main__':
    process()
