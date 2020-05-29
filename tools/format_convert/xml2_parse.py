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
        print("xmldom.parse:", type(domobj))

        # 得到元素对象
        elementobj = domobj.documentElement
        print("domobj.documentElement:", type(elementobj))

        # 获得子标签
        subElementObj = elementobj.getElementsByTagName("point")
        print("getElementsByTagName:", type(subElementObj))

        # 存储每个点的x，y坐标
        landmark = np.zeros((106,2))
        for i in range(len(subElementObj)):
            landmark[i, 0] = subElementObj[i].getAttribute("x")
            landmark[i, 1] = subElementObj[i].getAttribute("y")
        save_name = file_name.split(".xml")[0] + ".txt"
        save_path = os.path.join(save_dir, save_name)
        np.savetxt(save_path, landmark)
    return


if __name__ == "__main__":
    file_dir = "../../datasets/train/exercise/"
    save_dir = "../../datasets/train/landmark/"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    parse_xml(file_dir, save_dir)
