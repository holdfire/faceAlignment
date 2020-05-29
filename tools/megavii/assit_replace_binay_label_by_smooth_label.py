import os
import glob

path_label_list_src = '/ssd/cxzhao/code/scripts/quality/quality_data_self_label_v1/final/train_all_20191228_balance.txt'
path_label_list_dst = '/ssd/cxzhao/code/scripts/quality/quality_data_self_label_v1/final/train_all_20191228_smooth_balance.txt'
path_label_smooth = '/ssd/cxzhao/code/scripts/quality/quality_data_self_label_v1/txt/all_data_list_quality.txt'

def process():
    with open(path_label_smooth, 'r') as fid:
        lines = fid.readlines()
    print('num of smooth:', len(lines))
    smooth_dicts = {}
    for l, line in enumerate(lines):
        img_path, quality_str = line.strip().split()
        last_names_str = '/'.join(img_path.split('/')[-2:])
        smooth_dicts[last_names_str] = quality_str
    
    illegal_num = 0

    lines_res = []
    with open(path_label_list_src, 'r') as fid:
        lines = fid.readlines()
    print('num of src:', len(lines))
    for l, line in enumerate(lines):
        name_splits = line.strip().split()
        img_path = name_splits[0]
        last_names_str = '/'.join(img_path.split('/')[-2:])
        if last_names_str not in smooth_dicts.keys():
            illegal_num += 1
            print(illegal_num, img_path)
            continue
        quality_str = smooth_dicts[last_names_str]
        name_splits_new = [img_path, quality_str] + name_splits[2:]
        line_new = ' '.join(name_splits_new) + '\n'
        lines_res.append(line_new)

    print('num of dst:', len(lines_res))
    with open(path_label_list_dst, 'w') as fid:
        fid.writelines(lines_res)

if __name__ == '__main__':
    process()

