import os
import cv2
import numpy as np


if __name__ == "__main__":

    image_dir = "../../datasets/train/images"
    landmark_dir = "../../datasets/train/landmark"
    save_dir = "../../datasets/train/save/"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    file1 = os.listdir(image_dir)
    file1.sort()
    file2 = os.listdir(landmark_dir)
    file2.sort()
    file = zip(file1, file2)

    for (image_name, landmark_name) in file:
        print(image_name, landmark_name)
        if image_name.split(".jpg")[0] == landmark_name.split(".txt")[0]:

            image_path = os.path.join(image_dir, image_name)
            img = cv2.imread(image_path)

            landmark_path = os.path.join(landmark_dir, landmark_name)
            landmark = np.loadtxt(landmark_path, dtype="float", skiprows=0).astype("int")
            print(landmark.shape)

            for ld in landmark:
                img = cv2.circle(img, (ld[0], ld[1]), radius=2, color=(0,255,0), thickness=-1)

            save_path = os.path.join(save_dir, image_name + "_landmark.jpg")
            cv2.imwrite(save_path, img)


