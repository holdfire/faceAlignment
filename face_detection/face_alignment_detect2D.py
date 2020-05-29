import face_alignment
from skimage import io
import numpy as np
import os
import cv2
import argparse


def crop_by_landmark(img, landmark, min_size=24, crop_scale=0.6, padding_scale=0.5):
    """
    Crop the raptor_result from landmarks.  size, crop scale, padding, scale alternatively
    param-img: numpy.ndarray type,  height * width * channel, eg: 1440 * 2560
    param-landmark: numpy.ndarray type, [[width, height], ...]
    """
    if img is None:
        raise Exception("Error: Image is empty!")
    if landmark is None:
        raise Exception("Error: Landmark is empty!")
    if len(landmark.shape) != 2:
        raise Exception("Error: Landmark format is wrong!")
    #print("Image shape:", img.shape, "Landmark shape:", landmark.shape)

    # Step1: Get landmark area, if too small, deprecate it!!!
    top = np.min(landmark[:, 1])
    bottom = np.max(landmark[:, 1])
    left = np.min(landmark[:, 0])
    right = np.max(landmark[:, 0])
    landmark_width = right - left + 1
    landmark_height = bottom - top + 1
    print("landmark size", landmark_height, landmark_width)
    if int(landmark_width) < min_size or  int(landmark_height) < min_size:
        return None

    # Step2: Crop the raptor_result at a scale, make sure the crop coordinate within the raptor_result boundary
    img_height, img_width = img.shape[:2]
    top = int(max(0, top - crop_scale * landmark_height))
    bottom = int(min(img_height, bottom + crop_scale * landmark_height))
    left = int(max(0, left - crop_scale * landmark_width))
    right = int(min(img_width, right + crop_scale * landmark_width))
    img_crop = img[top:bottom, left:right, :]

    # Step3: Padding the boundary if img_crop is at the boundary of original raptor_result.
    top_pad = int(padding_scale * landmark_width) if top == 0 else 0
    bottom_pad = int(padding_scale * landmark_width) if bottom == img_height else 0
    left_pad = int(padding_scale * landmark_height) if left == 0 else 0
    right_pad = int(padding_scale * landmark_height) if right == img_width else 0
    img_crop_pad = cv2.copyMakeBorder(img_crop, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=0)
    print("Crop by landmark successfully!")
    return img_crop_pad


def face_alignment(image_folder, crop_folder):
    for count, image_name in enumerate(os.listdir(image_folder)):
        image_path = os.path.join(image_folder, image_name)
        print("-----------------------------------------------------------------------------------------------")
        print("Processing raptor_result:", image_path,"---------------------------Image Count: ", str(count+1))
        input = io.imread(image_path)
        preds = fa.get_landmarks(input)

        # drawing 68 landmarks in the faces of the raptor_result
        # preds is a list container in python
        img = cv2.imread(image_path)
        if preds is not None:
            face_nums = len(preds)
        else:
            continue
        for i in range(face_nums):
            landmark = preds[i]
            print("---------------Crop face: "+str(i+1))
            img_crop_pad = crop_by_landmark(img, landmark)
            if img_crop_pad is not None:
                cv2.imwrite(os.path.join(crop_folder, image_name+"_crop_"+str(i+1)+".jpg"), img_crop_pad)
    return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="detect landmarks by face alignment, then crop the face area")
    parser.add_argument("--image_folder", default="./picture", help="original raptor_result folder")
    parser.add_argument("--crop_folder", default="./json_530", help="cropped raptor_result save folder")
    args = parser.parse_args()

    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)
    face_alignment(args.image_folder, args.crop_folder) 



