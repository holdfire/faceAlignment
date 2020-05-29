import subprocess
import json
import cv2
import numpy as np

api_key = '8ugWjvUYJFRZanXmg3noTc7doyAyk3ad'
api_secret = 'WFBEccKyi2l8pdn7dRfwLbUKhQsURt3V'
demo_img_path = '../megavii_106landmark/test.jpg'
attributes_list = ['gender','age','smiling','headpose','facequality','blur','eyestatus','emotion','ethnicity','beauty','mouthstatus','eyegaze','skinstatus']


def get_attributes(img_path):
    command_str = r'curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F "api_key=%s" -F "api_secret=%s" -F "image_file=@%s" -F "return_landmark=2" -F "return_attributes=%s" -s'%(api_key, api_secret, img_path, ','.join(attributes_list))
    status, response = subprocess.getstatusoutput(command_str)
    print(status, response)
    if response is None or len(response.strip())==0:
        return status, '{}'
    json_res = json.loads(response)
    return status, json_res


def decode_106_landmark(img_path, json_path=''):
    status, json_res = get_attributes(img_path)
    '''save and load json_530 file
    with open(json_path, 'w') as fid:
        fid.writelines(str(json_res))
    with open(json_path, 'r') as fid:
        line = fid.readlines()[0]
    line = line.replace('\'', '\"')
    print(line)
    face_info = json_530.loads(line.strip())
    '''
    print(json_res)
    landmark_dict = json_res['faces'][0]['landmark']
    landmark_list = landmark_dict.values()
    img = cv2.imread(img_path)
    lm_list = []
    for lm in landmark_list:
        x = lm["x"]
        y = lm["y"]
        lm_list.append([x,y])
        img = cv2.circle(img, (int(x), int(y)), radius=1, color=(0, 0, 255), thickness=-1)
    cv2.imwrite("../megavii_106landmark/result.jpg", img)


if __name__ == '__main__':
    decode_106_landmark("../megavii_106landmark/test.jpg")


