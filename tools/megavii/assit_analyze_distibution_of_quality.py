import os
import glob

path_scores = '/ssd/cxzhao/code/scripts/quality/quality_data_self_label_v1/txt/all_data_list_quality.txt'

num_parts = 10
dists = [0 for x in range(num_parts)]

def process():
    with open(path_scores, 'r') as fid:
        lines = fid.readlines()
    for l, line in enumerate(lines):
        img_path, quality_str = line.strip().split()
        quality = float(quality_str)
        part = int(quality * num_parts)
        dists[part] += 1

    for p, part_num in enumerate(dists):
        print(p, part_num)

if __name__ == '__main__':
    process()
