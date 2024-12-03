## Need requests library to download image file from server
import requests

## Needed to determine if imagefile is HEIC
import os.path

## exif was deprecated in favour of pillow as it can handle more image formats
## from exif import Image

from PIL import Image, ExifTags
from PIL.ExifTags import GPS

## Needed to extract exif data from iphone HEIC file format
from pillow_heif import register_heif_opener

def image_date(image_path):
    file_ext = os.path.splitext(image_path)[1]
    if file_ext == ".heic":
        register_heif_opener()
    image = Image.open(image_path)
    return(image.getexif())
    
image1 = ("test_data/image1.heic")
print(image_date(image1))

##def polyline(lat, long):
##    return polyline
