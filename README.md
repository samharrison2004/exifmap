# exifmap
A tool for plotting exifdata extracted from image files to a map.

# The pitch
Imagine you are a forensic investigator. You have recovered several image files from a digital camera and you wish to visualise where the photos were taken and when. This project aims to create a tool that:
+ Extracts exifdata from a selection of image files
+ Sorts the files by the time they were taken
+ Creates a polyline using the latitude and longitude data extracted from the images
+ Plots the polyline onto a downloadable image file

This project makes use of the MapBox API. I chose it over the Google Maps API as it can be used (pretty much) for free by individuals. 

Using this program will require you to [sign up](https://www.mapbox.com/) and add your [API key](https://docs.mapbox.com/help/getting-started/access-tokens/) to the program.
