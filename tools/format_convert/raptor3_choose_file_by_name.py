import os
import shutil
import numpy as np


def choose_file(file_list, src_file_dir, dst_file_dir):
    name_list = np.loadtxt(file_list, dtype='str')
    for i in range(len(name_list)):
        name_list[i] = name_list[i].split(".jpg")[0]
    print(name_list[:10])

    for file in os.listdir(src_file_dir):
        if file.split(".jpg")[0] in name_list:
            src_path = os.path.join(src_file_dir, file)
            dst_path = os.path.join(dst_file_dir, file)
            shutil.copyfile(src_path, dst_path)

if __name__ == "__main__":
    file_list = "../../datasets/test/json1/image_list.txt"

    src_file_dir = "../../tmp/raptor_result"
    dst_file_dir = "../../datasets/test/image1"
    if not os.path.exists(dst_file_dir):
        os.mkdir(dst_file_dir)

    choose_file(file_list, src_file_dir, dst_file_dir)

