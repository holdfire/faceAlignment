import os
import numpy as np
import xml.dom.minidom as xmldom

def parse_xml(file_dir, save_dir):
    for file_name in os.listdir(file_dir):
        if file_name.split(".")[-1] != "xml":
            continue
        file_path = os.path.join(file_dir, file_name)

        # 得到文档对象
        domobj = xmldom.parse(file_path)
        # 得到所有元素对象
        elementobj = domobj.documentElement

        # 通过标签名width和height获得文本
        width_obj = elementobj.getElementsByTagName("width")[0]
        width = width_obj.childNodes[0].data
        height_obj = elementobj.getElementsByTagName("height")[0]
        height = height_obj.childNodes[0].data

        # 通过标签名point获得属性值
        subElementObj = elementobj.getElementsByTagName("point")
        # 获取每个点元素的属性：x，y
        landmark = np.zeros((106, 2))
        for i in range(len(subElementObj)):
            landmark[i, 0] = float(subElementObj[i].getAttribute("x")) / float(width)
            landmark[i, 1] = float(subElementObj[i].getAttribute("y")) / float(height)

        save_name = file_name.split(".xml")[0] + ".txt"
        save_path = os.path.join(save_dir, save_name)
        np.savetxt(save_path, landmark)
    print("{0:1d} xml files have been converted into relative coordinates".format(len(os.listdir(file_dir))))
    return


if __name__ == "__main__":
    file_dir = "../../dataset_train/train_inspect4/landmark_xml/"
    save_dir = "../../dataset_train/train_inspect4/landmark_relative/"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    parse_xml(file_dir, save_dir)
