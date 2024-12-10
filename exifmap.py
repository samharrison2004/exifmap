## Need requests library to download image file from server
import requests

## Needed to give the program command line functionality
import argparse

## Needed to determine if imagefile is HEIC
import os

## Needed to sort files by the datetime they were created
from datetime import datetime

## exif was deprecated in favour of pillow as it can handle more image formats (specifically the iPhone .heic format)
## from exif import Image

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

## Needed to extract exif data from iphone HEIC file format
from pillow_heif import register_heif_opener

## Filetypes that pillow can process. Enables the program to filter invalid filetypes. Tuple to save memory
accepted_filetypes = (".heic", ".png", ".jpeg", ".jpg", ".ppm", ".tiff", ".gif", ".bmp")

def find_image_files(path, accepted_filetypes):
    good_files = []
    file_list = os.listdir(path)
    for file in file_list:
        file_extension = os.path.splitext(file)[1]
        for good_file_ext in accepted_filetypes:
            if file_extension == good_file_ext:
                good_files.append(file)
    return good_files

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
        if decoded == ("DateTime"): ## If the key is 'DateTime'
            
            datetime_str = value
            return(datetime)
            """
            date,time = datetime_str.split() ## Split the value by the space
            year,month,day = date.split(":") 
            hour,minute,second = time.split(":")
            datetime = [year, month, day, hour, minute, second] ## Turns the data into a list going from year to second, left to right
            return(datetime)
            """

## Function for extracting GPS information from exif data 
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

def sort_files(file_dictionary):
    sorted_filenames = []
    datetime_format = "%y:%m:%d %H:%M:%S" ## The format the exif datetime comes in
    datetime_list = file_dictionary.values()
    datetime_list = sorted(datetime_list, key = lambda x: datetime.strptime(x,datetime_format))
    for i in range(len(datetime_list)):
        for file,datetime in file_dictionary:
            if datetime == datetime_list[i]:
                sorted_filenames.append(file)
    return sorted_filenames
    
    '''
    for key in exif_table["GPSInfo"].keys():
        decode = GPSTAGS.get(key,key)
        gps_info[decode] = exif_table['GPSInfo'][key]
    print (gpsinfo)
    '''
image1 = ("test_data/image1.heic")

parser = argparse.ArgumentParser()

## Argument for selecting the path of the folder containing the images the user wants to extract GPS data from. If none is provided exifmap will use the current working directory
parser.add_argument("-f","--folderpath", type=str, help = "The path of the folder containing the image files you wish to use. If not specified, exifmap will search in the current working directory")

## Argument for naming a file to output the polyline string to. If the flag is selected, the program will save the polyline to a text file named polyline.txt, unless the user specifies otherwise
parser.add_argument("-p","--polyline", type=str, help = "Name of file to output polyline string to. If flag is used but no name is provided exifmap will name a file polyline.txt containing the polyline")

args = parser.parse_args()

user_wd = os.getcwd() ## Sets user working directory to the current working directory

if args.folderpath: ## If user selects specific directory
    os.chdir(args.folderpath) ## Change directory to that specified by user
    files_path = os.getcwd() ## Set the filepath equal to that directory
else: 
    files_path = user_wd ## Set the filepath equal to current working directory

good_files = find_image_files(files_path, accepted_filetypes) ## Finds the 'good' files 
files_by_date = {}
datetime_list = []
for file in good_files:
    file_exif_data = exif_data(file)
    file_datetime = extract_datetime(file_exif_data)
    files_by_date[file] = file_datetime
sort_files(files_by_date)
