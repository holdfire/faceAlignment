import os
import cv2
import numpy as np


def landmark_98_to_5(landmark98_path, landmark5_path):
    """
    从人脸98个关键点中选出5个：左眼，右眼，鼻尖，左嘴角，右嘴角
    """
    # 读取98个关键点文件后，生成一个list文件
    landmark98 = []
    with open(landmark98_path, 'r') as f:
        text = f.readlines()
        for line in text:
            landmark98.append(line)

    # 从98个点中选取5个目标点，保存到指定文件中
    order = [74, 83, 54, 84, 90]
    with open(landmark5_path, 'w') as f:
        for i in order:
            f.writelines(landmark98[i])
    return


if __name__ == "__main__":
    landmark98_path = "../dataset_train/train_inspect4/landmark_relative/facetrack_20200407135638_14268.txt"
    landmark5_path = "../dataset_train/train_inspect4/landmark_relative_5/facetrack_20200407135638_14268.txt"
    # if not os.path.exists(landmark5_path):
    #     os.mkdir(landmark5_path)

    landmark_98_to_5(landmark98_path, landmark5_path)