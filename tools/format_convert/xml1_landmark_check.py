import os
import numpy as np

def landmark_check(file_dir):
    error_log = []
    for file_name in os.listdir(file_dir):
        if file_name == "0_error_log.txt":
            continue
        if file_name.split(".")[-1] != "txt":
            continue
        file_path = os.path.join(file_dir, file_name)
        landmark = np.loadtxt(file_path)
        landmark = landmark.astype(np.int32)
        if landmark.shape != (106, 2):
            error_log.append(file_name + "  的点数为:  " + str(landmark.shape[0]))
        for i in range(16):
            if (landmark[i, 0] > landmark[i+1, 0]) | (landmark[i, 1] > landmark[i+1, 1]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(16, 32):
            if (landmark[i, 0] > landmark[i+1, 0]) | (landmark[i, 1] < landmark[i+1, 1]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(33, 37):
            if (landmark[i, 0] > landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(38, 41):
            if (landmark[i, 0] < landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(42, 46):
            if (landmark[i, 0] > landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(46, 50):
            if (landmark[i, 0] < landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(51, 54):
            if (landmark[i, 1] > landmark[i+1, 1]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(55, 60):
            if (landmark[i, 1] > landmark[i+1, 1]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(60, 65):
            if (landmark[i, 1] < landmark[i+1, 1]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(66, 70):
            if (landmark[i, 0] > landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(70, 73):
            if (landmark[i, 0] < landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(75, 79):
            if (landmark[i, 0] > landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(84, 90):
            if (landmark[i, 0] > landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(90, 95):
            if (landmark[i, 0] < landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(96, 100):
            if (landmark[i, 0] > landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
        for i in range(100, 103):
            if (landmark[i, 0] < landmark[i+1, 0]):
                error_log.append(file_name + "  的第  " + str(i+1) + "  号点标记错误！")
    return error_log




if __name__ == "__main__":
    file_dir = "../../dataset_train/train_inspect3/landmark_standard/"
    save_path = os.path.join(file_dir, "0_error_log.txt")
    error_log = landmark_check(file_dir)
    error_log = np.array(error_log)
    np.savetxt(save_path, error_log, fmt="%s")