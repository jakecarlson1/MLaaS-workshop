import requests
from urllib.request import urlopen
from email.mime.image import MIMEImage

def style_transfer(image_name, image):
    # Make a post request to the stylizing service
    r = requests.post("http://delegator:8000/Style", files = {'image': image})
    # Parse out the relative path on the endpoint where the stylized image is stored
    path = str(r.content)[2:-1]

    # Load the stylized image
    style_transfer_image_bytes = urlopen("http://delegator:8000" + path).read()

    # Process the image into a MIME image to send back over MMS
    image = MIMEImage(style_transfer_image_bytes)
    image.add_header('Content-Disposition', "attachment; filename= stylized_%s" % image_name)
    return image
