import subprocess
import json

'''
command_str = \
r'curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F "api_key=<api_key>" -F "api_secret=<api_secret>" -F "image_file=@image_file.jpg" -F "return_landmark=1" -F "return_attributes=gender,age"'
print(command_str)
print(subprocess.getstatusoutput('cat bin/junk'))
'''
api_key = '8ugWjvUYJFRZanXmg3noTc7doyAyk3ad'
api_secret = 'WFBEccKyi2l8pdn7dRfwLbUKhQsURt3V'
'''
api_key = 'S34PkcPnCymGtb5PKqrKAqKzdOSareBR'
api_secret = 'si6BAvwcgge28DG5Fe0R-DWH3l6KSXNy'
'''
demo_img_path = 'test.jpg'

attributes_list = ['gender','age','smiling','headpose','facequality','blur','eyestatus','emotion','ethnicity','beauty','mouthstatus','eyegaze','skinstatus']

def process_():
    #command_str = \
    #r'curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F "api_key=%s" -F "api_secret=%s" -F "image_file=@%s" -F "return_landmark=1" -F "return_attributes=facequality,headpose"  -F "return_attributes=gender,age" -s'%(api_key, api_secret, demo_img_path)
    command_str = r'curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F "api_key=%s" -F "api_secret=%s" -F "image_file=@%s" -F "return_landmark=1" -F "return_attributes=%s" -s'%(api_key, api_secret, demo_img_path, ','.join(attributes_list)) 

    status, response = subprocess.getstatusoutput(command_str)
    print(status, response)
    #print(response)
    json_res = json.loads(response)
    print(json_res.keys())
    print(json_res['faces'][0]['face_token'])
    '''    
    face_token = json_res['faces'][0]['face_token']
    command_str = \
    r'curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/face/analyze" -F "api_key=%s" -F "api_secret=%s" -F "return_landmark=1" -F "face_tokens=%s" -s'%(api_key, api_secret, face_token)
    status_quality, response_quality = subprocess.getstatusoutput(command_str)
    print(status_quality, response_quality)
    json_quality = json_530.loads(response_quality)
    print(json_quality.keys())
    '''

def get_attributes(img_path):
    command_str = r'curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F "api_key=%s" -F "api_secret=%s" -F "image_file=@%s" -F "return_landmark=2" -F "return_attributes=%s" -s'%(api_key, api_secret, img_path, ','.join(attributes_list))
    status, response = subprocess.getstatusoutput(command_str)
    print(status, response)
    if response is None or len(response.strip())==0:
        return status, '{}'
    json_res = json.loads(response)
    return status, json_res

def get_attributes_json(img_path, json_path):
    status, json_res = get_attributes(img_path)
    with open(json_path, 'w') as fid:
        fid.writelines(str(json_res))
    return 1

def decode_face_quality_from_attributes_json(json_path):
    with open(json_path, 'r') as fid:
        line = fid.readlines()[0]
    line = line.replace('\'', '\"')
    print(line)
    face_info = json.loads(line.strip())
    
    if 'faces' not in face_info.keys() or  face_info['faces'] == []:
        return 0.0   
    bbox_info = face_info['faces'][0]['face_rectangle']
    left, top, width, height = bbox_info['left'], bbox_info['top'], bbox_info['width'], bbox_info['height']
    face_quality = face_info['faces'][0]['attributes']['facequality']['value']
    return face_quality


if __name__ == '__main__':
    process_()


