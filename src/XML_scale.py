#!/usr/bin/python3

import sys, re
from bs4 import BeautifulSoup as bs
import numpy as np

def main():

    file_path = sys.argv[1]
    scale_factor = float(sys.argv[2])
    output_path = sys.argv[3]

    xml_soup = bs(open(file_path, 'r'), 'xml')

    # FACES
    for faces in xml_soup.find_all('F'):
        for face in faces:
            
            # LOOPING THROUGH THE FACES
            face_list = [int(x) for x in face.split(" ")]
            
            face.replace_with(' '.join(map(str, face_list)))

    # POINTS
    for points in xml_soup.find_all('P'):
        for point in points:
            
            point_list = [float(x) for x in point.split(" ")]

            point_list[0] = "{:.12f}".format(point_list[0] * scale_factor)
            point_list[1] = "{:.12f}".format(point_list[1] * scale_factor)
            point_list[2] = "{:.4f}".format(point_list[2])
            
            point.replace_with(' '.join(map(str, point_list)))
    
    
    
    # WRITE OUT FILE
    with open(output_path, "w") as f:
    	f.write(str(xml_soup))


    print("\n")
    print("Number of surface: %s" % len(xml_soup.find_all("Surface")))
    print("Number of breaklines: %s" % len(xml_soup.find_all('Breakline')))
    print("Number of points: %s" % len(xml_soup.find_all('P')))
    print("Scale factor: %s" % scale_factor)


if __name__ == '__main__':
    main()
