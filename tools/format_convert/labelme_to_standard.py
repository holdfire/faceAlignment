#-*- coding:utf-8 -*-import os
import os
import json
import numpy as np

def json_to_array(json_path, save_path):
    with open(json_path) as f:
        json_res = json.load(f)
        image_name = json_res["imagePath"]
        shapes = json_res["shapes"]
        for shp in shapes:
            landmark_array = np.zeros((106, 2), dtype="float")
            if shp["status"] == "完成":
                annotations = shp["annotations"]
                for i, anno in enumerate(annotations):
                    order = int(float(anno["textContent"]))
                    coordinate = anno["annotationList"][0]
                    coordinate = list(map(lambda x: float(x), coordinate))
                    # assign coordinate to landmark array
                    landmark_array[order-1, 0] = coordinate[0]
                    landmark_array[order-1, 1] = coordinate[1]
                np.savetxt(os.path.join(save_path, image_name.split(".jpg")[0]+".json_530"), landmark_array)
    return


if __name__ == "__main__":
    json_path = "../../datasets/test/test1/annotations.json_530"
    save_path = "../../tmp/test1_106_landmarks/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    json_to_array(json_path, save_path)
