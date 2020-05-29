import os
import cv2
import numpy as np

def transform_format(prefix, name_file,image_dir,  json_dir, save_list_path, save_image_dir, new_size=(112,112), scale = 1.4):
    image_name_list = np.loadtxt(name_file, dtype='str')
    result = []

    for i, json_name in enumerate(os.listdir(json_dir)):
        image_name = json_name.split(".json")[0]+".jpg"
        if image_name in image_name_list:
            ##### save absolute image path
            tmp = [prefix + image_name]

            ##### 通过边缘填充，把图像处理成正方形
            img = cv2.imread(os.path.join(image_dir, image_name))
            old_height, old_width = img.shape[:2]
            if old_height < old_width:
                img = cv2.copyMakeBorder(img, 0, old_width-old_height, 0, 0, cv2.BORDER_CONSTANT, value=0)
            elif old_height > old_width:
                img = cv2.copyMakeBorder(img, 0, 0, 0, old_height-old_width, cv2.BORDER_CONSTANT, value=0)

            ###### 从106个点中选取98个点
            json_file = np.loadtxt(os.path.join(json_dir, json_name))
            json_98 = np.zeros((98, 2))
            json_98[:55, :] = json_file[:55, :]
            json_98[55:60, :] = json_file[58:63, :]
            json_98[60:68, :] = json_file[66:74, :]
            json_98[68:76, :] = json_file[75:83, :]
            json_98[76:96, :] = json_file[84:104, :]
            json_98[96:98, :] = json_file[104:106, :]

            ###### 通过包含关键点区域矩形的中心点，构造一个新的正方形
            landmark_left = max(0, np.min(json_98[:,0]))
            landmark_right = np.max(json_98[:, 0])
            landmark_top = max(np.min(json_98[:, 1]), 0)
            landmark_bottom = np.max(json_98[:, 1])
            if (landmark_left<0) | (landmark_top<0) | (landmark_right>old_width) | (landmark_bottom>old_height):
                raise Exception("landmark error!!!!!!!")

            center_x = (landmark_left + landmark_right) / 2
            center_y = (landmark_top + landmark_bottom) / 2
            edge = max(landmark_right - landmark_left, landmark_bottom - landmark_top) * scale
            new_x1 = int(center_x - 0.5 * edge)
            new_y1 = int(center_y - 0.5 * edge)
            new_x2 = int(center_x + 0.5 * edge)
            new_y2 = int(center_y + 0.5 * edge)

            ##### 把关键点坐标换了, 归一化，压成list，存一下
            json_98[:, 0] = (json_98[:, 0] - new_x1) / (edge + 1)
            json_98[:, 1] = (json_98[:, 1] - new_y1) / (edge + 1)
            json_98 = json_98.reshape((-1))
            if json_98.any() < 0:
                raise Exception("rectangle error!!!!!!!")
            for coord in json_98:
                tmp.append(coord)
            for num in range(9):
                tmp.append(0)
            result.append(tmp)

            ##### reshape image
            img_new = img[new_y1:new_y2+1, new_x1:new_x2+1,:].copy()
            img_new = cv2.resize(img_new, new_size)
            cv2.imwrite(os.path.join(save_image_dir, image_name), img_new)
    np.savetxt(save_list_path, result, fmt='%s')
    return


if __name__ == "__main__":

    prefix = "/home/projects/git_repositoriy/pfld_pytorch/data/test1/imgs/"

    name_file = "../../datasets/test/json1/image_list.txt"
    image_dir = "../../datasets/test/image1/"
    json_dir = "../../datasets/test/json1/"

    save_list_path = "../../datasets/test/test1/list.txt"
    save_image_dir = "../../datasets/test/test1/imgs"
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)

    transform_format(prefix, name_file, image_dir, json_dir, save_list_path, save_image_dir)



