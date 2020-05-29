import os
import glob

path_img_list = '/ssd/cxzhao/data/quality_for_clean/tidy_by_yaoqi/test_list.txt'
path_pair_list = '/ssd/cxzhao/data/quality_for_clean/tidy_by_yaoqi/test_list_pairs.txt'

prefix = '/ssd/cxzhao/data/quality_for_clean/tidy_by_yaoqi'
postfix = '/ssd/cxzhao/data/quality_for_clean/tidy_by_yaoqi_json'

def process():
    with open(path_img_list, 'r') as fid:
        lines = fid.readlines()
    lines_res = []
    for l, line in enumerate(lines):
        img_path = line.strip()
        json_path = img_path.replace(prefix, postfix)[:-4] + '.txt'
        os.makedirs(os.path.split(json_path)[0], exist_ok=True)
        line_new = img_path + ' ' + json_path + '\n'
        lines_res.append(line_new)

    with open(path_pair_list, 'w') as fid:
        fid.writelines(lines_res)

if __name__ == '__main__':
    process()
