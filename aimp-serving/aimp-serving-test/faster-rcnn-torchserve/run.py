from __future__ import print_function

import io
import os
import time
import base64
import json
import time
import cv2 
import requests
import pickle
import onepanel.core.api
from onepanel.core.api.rest import ApiException
import onepanel.core.auth
from pprint import pprint

# MUST import AIMP python SDK
# import upper dir's python file
import sys
sys.path.append("../..") 
sys.path.append("..") 
import aimpInferWorkFlowSDK

#start init the aimpinferWorkFlowSDK
aimpPredict=aimpInferWorkFlowSDK.aimpInfer()
aimpPredict.namespace = 'mp'
aimpPredict.model_name = 'faster-rcnn-torchserve'
aimpPredict.getAccess()
access_token=aimpPredict.api_access_token
infer_host_FQDN=aimpPredict.infer_host_FQDN
infer_endpoint=aimpPredict.infer_endpoint
#end init the aimpinferSDK

import base64
image = open('./cat.jpg', 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.b64encode(image_read)
bytes_array = image_64_encode.decode('utf-8')

data = {
    'instances': [
        {'data': bytes_array}
    ]
}

headers = {
    'onepanel-access-token': access_token,
    'Content-Type': 'application/json',
    'Host': infer_host_FQDN,
}
print('---api_predict_endpoint and headers---')
print (infer_endpoint)
pprint(headers)
print('\n')
print('---Prediction RESULTS---')
# original predict URL
#r = requests.post(endpoint, headers=headers, data=data, verify=False)
# skip cert check
r = requests.post(infer_endpoint, headers=headers, data=json.dumps(data), verify=False)
result = r.json()
pic_result = result['predictions'][0] #the result of one picture

print(pic_result)

##screen result
list1 = []
for i in pic_result:
    if i['score'] > 0.5:
        list1.append(i)

#draw the frame
img = cv2.imread('./cat.jpg')

for ret in list1:
    for k, v in ret.items():
        if k == 'score':
            pass
        else:
            x1, y1, x2, y2 = [int(i) for i in v]
        
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)
            img = cv2.putText(img,k,(x1-5,y1-10),0,1,(0,0,0),1)

cv2.imwrite('./cat_det.jpg', img)
 

