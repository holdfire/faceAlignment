import cv2

def crop_from_landmark(img, bbox, crop_scale=1.3, new_size=(112, 112)):
    """
    给定原图和人脸bbox框，首先依据该框的中心裁剪一个正方形出来；然后将该正方行缩放到new_size
    """
    # Step0：定义一下原图的尺寸，防止裁剪时坐标越界
    img_height, img_width = img.shape[:2]

    # Step1：确定原bbox框的中心坐标
    x1, y1, x2, y2 = bbox
    center_x = (x1 + x2) / 2.0
    center_y = (y1 + y2) / 2.0

    # Step2：原bbox框最大边长的crop_scale倍，就是要裁剪的正方形的边长
    face_width = x2 - x1
    face_height = y2 - y1
    edge = max(face_height, face_width) * crop_scale
    edge = min(edge, min(2*center_x, min(2*center_y, min(2*(img_width-center_x), 2*(img_height-center_y)))))

    # Step3：确定裁剪正方形的左上角和右下角坐标后，如果坐标没越界就可以裁了
    new_x1 = max(0, int(center_x - 0.5 * edge))
    new_y1 = max(0, int(center_y - 0.5 * edge))
    new_x2 = min(int(center_x + 0.5 * edge), img_width-1)
    new_y2 = min(int(center_y + 0.5 * edge), img_height-1)
    print("crop_bbox:[{0},{1},{2},{3}]".format(str(new_x1), str(new_y1), str(new_x2), str(new_y2)), "edge: ", edge)
    new_face = img[new_y1:new_y2, new_x1:new_x2, :].copy()

    # Step4：将裁剪出来的正方形人脸缩放到固定尺寸
    target_face = cv2.resize(new_face, new_size)
    return [new_x1, new_y1, new_x2, new_y2], target_face


if __name__ == "__main__":
    image_path = "./test.jpg"
    img = cv2.imread(image_path)
    bbox = [138, 90, 303, 307]

    crop_bbox, target_face = crop_from_landmark(img, bbox)
    cv2.imwrite("cropped_image.jpg", target_face)