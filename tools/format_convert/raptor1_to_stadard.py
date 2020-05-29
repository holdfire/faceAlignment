#-*- coding:utf-8 -*-import os
import os
import json
import numpy as np
import cv2


def json_to_array(json_path, save_dir):
    with open(json_path) as f:
        json_res = json.load(f)
        result = json_res["result"]
        error_log = []
        target_image_list = []

        for task in result:
            landmark_array = np.zeros((106, 2))
            image_name = task["docName"]
            width = task["width"]
            height = task["height"]

            if task["status"] == "完成":
                member = task["member"]
                if (member == "user9") | (member == "user10") | (member == "user11") | (member == "user13") | (member == "user16")| (member == "user17"):
                #if (member == "user12") | (member == "user15"):
                    annotations = task["annotations"]
                    print("current raptor_result name------:", image_name, "   ", member)
                    for i, anno in enumerate(annotations):
                        order = int(float(anno["textContent"]))
                        coordinate = anno["annotationList"][0]
                        coordinate = list(map(lambda x: float(x), coordinate))
                        # assign coordinate to landmark array
                        if (landmark_array[order-1, 0] > 0.01):
                            error_log.append(member + "  " + image_name + "  " + "标记点号 " + str(order)+ "  错误")
                            #error_log.append(image_name)

                        landmark_array[order-1, 0] = str(coordinate[0])
                        landmark_array[order-1, 1] = str(coordinate[1])
                    if i != 105:
                        error_log.append(member + "  " + image_name + "  " + "标记点的数目是: " + str(i+1))
                    # if not image_name in error_log:

                    target_image_list.append(image_name)
                     # 输出1：把每个合格的标准文件单独保存成json文件
                    np.savetxt(os.path.join(save_dir, image_name.split(".jpg")[0]+".json"), landmark_array, fmt='%s')
        # 输出2：把错误的信息保存为日志
        error_log = np.array(error_log, dtype='str')
        np.savetxt(os.path.join(save_dir, "error_log.txt"), error_log, fmt='%s')

        # 输出3：把符合要求的图片名称保存一下
        target_image_list = np.array(target_image_list, dtype='str')
        np.savetxt(os.path.join(save_dir, "image_list.txt"), target_image_list, fmt='%s')
    return



if __name__ == "__main__":
    json_path = "../../tmp/raptor_result/annotations.json"

    save_path = "../../datasets/test/json1/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    json_to_array(json_path, save_path)
