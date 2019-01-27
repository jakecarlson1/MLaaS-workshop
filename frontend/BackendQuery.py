import requests
import ast
from urllib.request import urlopen
from email.mime.image import MIMEImage

def style_transfer(image_name, image):
    r = requests.post("http://localhost:8000/Style", data = {'image': image})
    print(str(r))
    r = requests.post("http://localhost:8000/Return", data = {'image': image})
    print("Response from backend: " + str(r))
    path = ast.literal_eval(str(r.content)[2:-1])["image"]
    style_transfer_image_bytes = urlopen("http://localhost:8000" + path).read()
    image = MIMEImage(style_transfer_image_bytes)
    image.add_header('Content-Disposition', "attachment; filename= stylized_%s" % image_name)
    return image
