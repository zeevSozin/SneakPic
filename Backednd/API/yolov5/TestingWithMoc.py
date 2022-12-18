import yoloDetectionByImage as yolo
import json

result=yolo.DetectByImagesClassOnly(['./testing/images/skiVecation1.jpg','./testing/images/traffic.jpg'])
#result=yolo.DetectByImagesClassOnly(['./testing/images/skiVecation1.jpg'])
# result=yolo.DetectByImageReturnClassOnly(['./testing/images/skiVecation1.jpg'])
#json_formatted_str = json.dumps(result, indent = 2)
print(result)
print(type(result))

