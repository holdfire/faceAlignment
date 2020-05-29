import os
import argparse
import glob
import numpy as np
import cv2

parser = argparse.ArgumentParser(description="Draw boxes and landmarks in original raptor_result")
parser.add_argument("--dsn", "--dataset_name", default="draw_landmark_106_jd_rect", help="original raptor_result folder")
args = parser.parse_args()

dataset_path = os.path.join("../../datasets", args.dsn)
if not os.path.exists(dataset_path):
    print("the dataset",  args.dsn, "does not exist")

def check_result_folder():
    result_path = os.path.join("../../datasets/results", args.dsn)
    # rect folder exist?
    if not os.path.exists(os.path.join(result_path, "rect")):
        print("the results/"+args.dsn,  "/rect folder does not exist")
    if not os.path.exists(os.path.join(result_path, "landmark")):
        print("the results/"+args.dsn,  "/landmark folder does not exist")
    if not os.path.exists(os.path.join(result_path, "picture_crop")):
        print("the results/"+args.dsn,  "/picture_crop folder does not exist")
    rect_path = os.path.join(result_path, "rect")
    landmark_path = os.path.join(result_path, "landmark")
    picture_crop_path = os.path.join(result_path, "picture_crop")
    return result_path, rect_path, landmark_path, picture_crop_path


def origin_draw_rect_landmark():
    '''
    draw face rect and landmark of raptor_result in dataset path
    '''
    # check the json_530 folder information
    result_path, rect_path, landmark_path, picture_crop_path = check_result_folder()
    # save folder
    draw_landmark_path = os.path.join(result_path, "draw_landmark")
    if not os.path.exists(draw_landmark_path):
        os.mkdir(draw_landmark_path)

    for image_name in os.listdir(dataset_path):
        image_path = os.path.join(dataset_path, image_name)
        img = cv2.imread(image_path)
        print("Drawing--------", image_path, "--------  Original raptor_result shape:", img.shape)
        # recognize corresponding rectangle files and landmarks files
        img_rects = glob.glob(rect_path + "/" + image_name + "*.rect")
        img_landmarks_set = glob.glob(landmark_path + "/" + image_name + "*.txt")
        # draw rectangle and landmarks
        a = np.loadtxt(img_rects[0], dtype="str", delimiter=" ")
        print("face nums:", len(img_rects))
        for rect_path in img_rects:
            rect = np.loadtxt(rect_path, dtype="str", delimiter=" ").astype("int")
            img = cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (255,0,0), 2)
        for landmarks_path in img_landmarks_set:
            landmarks = np.loadtxt(landmarks_path, dtype="float", delimiter=" ", skiprows=0).astype("int")
            for landmark in landmarks:
               img = cv2.circle(img, (int(landmark[0]), int(landmark[1])), radius=2, color=(0,255,0), thickness=-1)
        img_save_path = os.path.join(draw_landmark_path, image_name+"_draw_rect_landmark.jpg")
        cv2.imwrite(img_save_path, img)
    return


if __name__ == "__main__":
    origin_draw_rect_landmark()







