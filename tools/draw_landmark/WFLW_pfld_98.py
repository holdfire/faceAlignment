import os
import numpy as np
import cv2


if __name__ == "__main__":
    # for pfld format data
    list_path = "../../datasets/test/test1/list.txt"
    item = np.loadtxt(list_path, dtype='str')[508]
    image_dir = '../../datasets/test/test1/imgs/'
    image_name = item[0].split("/")[-1]
    image_path = os.path.join(image_dir, image_name)

    save_path = 'tmp.jpg'

    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    landmark = np.array(item[1:197], dtype='float32')
    landmark = landmark.reshape((98,2))
    landmark = landmark * [width, height]
    landmark = landmark.astype(np.int32)

    for (x,y) in landmark:
        img = cv2.circle(img, (x,y), radius=1, color=(0, 255, 0), thickness=-1)

    #save_path = os.path.join(save_dir, image_name + "_landmark.jpg")
    cv2.imwrite(save_path, img)