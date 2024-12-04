## Need requests library to download image file from server
import requests

## Needed to determine if imagefile is HEIC
import os.path

## exif was deprecated in favour of pillow as it can handle more image formats
## from exif import Image

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

## Needed to extract exif data from iphone HEIC file format
from pillow_heif import register_heif_opener

def exif_data(image_path):
    exif_data = {}
    file_ext = os.path.splitext(image_path)[1]
    if file_ext == ".heic":
        register_heif_opener()
    image = Image.open(image_path)
    exif_data = image.getexif()
    return(exif_data)

## Function for finding the date/time the image was taken. Using the exifdata as opposed to the os module ensures
## accuracy, as exifdata is baked into the image
def extract_datetime(exif_data):
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag,tag)
        if decoded == ("DateTime"):
            datetime_str = value
            date,time = datetime_str.split()
            year,month,day = date.split(":")
            hour,minute,second = time.split(":")
            datetime = [year, month, day, hour, minute, second] ## Turns the data into a list going from year to second, left to right
            return(datetime)

def extract_gps(exif_data):
    exif_table = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "DateTimeOriginal":
            gps_info = {}
            for t in value:
                gps_decoded = GPSTAGS.get(t,t)
                gps_info[gps_decoded] = value
        exif_table[decoded] = value

    print (exif_table)
    
    
    '''
    for key in exif_table["GPSInfo"].keys():
        decode = GPSTAGS.get(key,key)
        gps_info[decode] = exif_table['GPSInfo'][key]
    print (gpsinfo)
    '''
image1 = ("test_data/image1.heic")
exifdata = exif_data(image1)
datetime = extract_datetime(exifdata)
print(datetime)
##def polyline(lat, long):
##    return polyline
