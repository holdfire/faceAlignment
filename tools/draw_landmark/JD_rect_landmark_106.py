import os
import glob
import numpy as np
import cv2


def origin_draw_rect_landmark(dataset_path, draw_save_path, num=10):
    picture_dir = os.path.join(dataset_path, "picture")
    rect_dir = os.path.join(dataset_path, "rect")
    landmark_dir = os.path.join(dataset_path, "landmark")

    for image_name in os.listdir(picture_dir)[:num]:
        image_path = os.path.join(picture_dir, image_name)
        img = cv2.imread(image_path)

        # find corresponding rectangle files and draw rectangles
        rect_path = glob.glob(rect_dir + "/" + image_name + "*.rect")
        if len(rect_path) < 1:
            continue
        rect = np.loadtxt(rect_path[0], dtype="str", delimiter=" ").astype("int")
        img = cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)

        # find corresponding landmarks files and draw landmarks
        landmarks_path = glob.glob(landmark_dir + "/" + image_name + "*.txt")[0]
        landmarks = np.loadtxt(landmarks_path, dtype="float", delimiter=" ", skiprows=1).astype("int")
        for landmark in landmarks:
           img = cv2.circle(img, (int(landmark[0]), int(landmark[1])), radius=2, color=(0,255,0), thickness=-1)

        img_save_path = os.path.join(draw_save_path, image_name+"_draw_rect_landmark.jpg")
        cv2.imwrite(img_save_path, img)
    return



if __name__ == "__main__":
    dataset_path = "../../dataset_public/JD-landmark/Train"
    draw_save_path = "../../dataset_public/JD-landmark/draw"
    if not os.path.exists(draw_save_path):
        os.mkdir(draw_save_path)

    origin_draw_rect_landmark(dataset_path, draw_save_path)







