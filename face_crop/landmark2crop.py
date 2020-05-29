import numpy as np
import cv2


def crop_by_landmark(img, landmark, min_size=16, crop_scale=0.6, padding_scale=0.5):
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
    print("Image shape:", img.shape, "Landmark shape:", landmark.shape)

    # Step1: Get landmark area, if too small, deprecate it!!!
    top = np.min(landmark[:, 1])
    bottom = np.max(landmark[:, 1])
    left = np.min(landmark[:, 0])
    right = np.max(landmark[:, 0])
    landmark_width = right - left + 1
    landmark_height = bottom - top + 1

    if int(landmark_width) < min_size | int(landmark_height) < min_size:
        return None

    # Step2: Crop the raptor_result at a scale, make sure the crop coordinate within the raptor_result boundary
    img_height, img_width = img.shape[:2]
    top = int(max(0, top - crop_scale * landmark_height))
    bottom = int(min(img_height, bottom + crop_scale * landmark_height))
    left = int(max(0, left - crop_scale * landmark_width))
    right = int(min(img_width, right + crop_scale * landmark_width))
    img_crop = img[top:bottom, left:right, :]
    print()

    # Step3: Padding the boundary if img_crop is at the boundary of original raptor_result.
    top_pad = int(padding_scale * landmark_width) if top == 0 else 0
    bottom_pad = int(padding_scale * landmark_width) if bottom == img_height else 0
    left_pad = int(padding_scale * landmark_height) if left == 0 else 0
    right_pad = int(padding_scale * landmark_height) if right == img_width else 0
    img_crop_pad = cv2.copyMakeBorder(img_crop, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=0)

    return img_crop_pad


if __name__ == "__main__":
    path = "./test.png"
    img = cv2.imread(path)
    landmark_path = "./test.txt"
    landmark = np.loadtxt(landmark_path, dtype="float", delimiter=" ", skiprows=0)
    img_crop_pad = crop_by_landmark(img, landmark)
    if img_crop_pad is not None:
        cv2.imwrite("json_530.png", img_crop_pad)