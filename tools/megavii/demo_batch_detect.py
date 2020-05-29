import os
import glob
import sys

from demo_detect_api import * 

'''
usage: python demo_batch_detect.py input_list_path.txt
input_list_path.txt contains lines: img_path out_put_path\n
'''

def process():
    input_list_path = sys.argv[1]
    with open(input_list_path, 'r') as fid:
        lines = fid.readlines()
    for l, line in enumerate(lines):
        if l < 509812:
            print(l, 'continue')
            continue
        name_splits = line.strip().split()
        if not len(name_splits) == 2:
            print(l, 'continue', len(name_splits), name_splits) 
        img_path, json_path = name_splits[:2]
        print('Processing: %d/%d, imagename: %s'%(l, len(lines), img_path))
        get_attributes_json(img_path, json_path)

if __name__ == '__main__':
    process()
    
