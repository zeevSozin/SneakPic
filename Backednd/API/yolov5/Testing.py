import torch
import json

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Images
#img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
#img = './testing/images/traffic.jpg'
img = './testing/images/skiVecation1.jpg'

# Inference
results = model(img)

# Results
#results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
#results.show()
jsonData=results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
json_object = json.loads(jsonData)
print(json.dumps(json_object, indent=1))

