import os
import cv2
import numpy as np

def draw_landmarks(image_path, landmark_path, save_path, skip_rows=0, put_text=False):
    """
    given image_path, landmark_path, draw landmarks on the image and save draw_image in save_path
    """
    img = cv2.imread(image_path)
    landmarks = np.loadtxt(landmark_path, dtype="float", skiprows=skip_rows).astype("int")
    for i, (x, y) in enumerate(landmarks):
        img = cv2.circle(img, (x, y), radius=1, color=(0, 255, 0), thickness=-1)
        if put_text:
            img = cv2.putText(img, str(i+1), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

    cv2.imwrite(save_path, img)
    return


def batch_draw_landmarks(image_dir, landmark_dir, save_dir):
    file1 = os.listdir(image_dir)
    file1.sort()
    file2 = os.listdir(landmark_dir)
    file2.sort()
    file = zip(file1, file2)

    for (image_name, landmark_name) in file:
        if not image_name.split(".jpg")[0] == landmark_name.split(".txt")[0]:
            raise Exception("输入图片名称和landmark名称不匹配")
        if image_name.split(".jpg")[0] == landmark_name.split(".txt")[0]:
            image_path = os.path.join(image_dir, image_name)
            landmark_path = os.path.join(landmark_dir, landmark_name)
            save_path = os.path.join(save_dir, image_name + "_landmark.jpg")
            draw_landmarks(image_path, landmark_path, save_path)
    return


if __name__ == "__main__":

    image_dir = "../../dataset_train/train_inspect4/images"
    landmark_dir = "../../dataset_train/train_inspect4/landmark_standard"
    save_dir = "../../dataset_train/train_inspect4/images_draw"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    batch_draw_landmarks(image_dir, landmark_dir, save_dir)
