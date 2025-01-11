import cv2
import numpy as np
import os
import easyocr

reader = easyocr.Reader(['en'])

result_image = cv2.imread("../dataset/images/000000894.png")

hieght, width, _ = result_image.shape

start_row = int(0.72 * hieght)
end_row = int(0.74 * hieght)

start_col = int(0.32 * width)
end_col = int(0.68 * width)

result_text = result_image[start_row:end_row, start_col:end_col]

skip = True
for file in os.listdir("../dataset/images"):
    # print(file)
    # if(file != "000000930.png" and file != "000000901.png" and file != "000000913.png"):
    #     continue

    if(file == "000000800.png"):
        skip = False

    if(skip):
        continue

    image = cv2.imread("../dataset/images/{}".format(file))

    image = cv2.resize(image, (width, hieght))

    current_text_ROI = None
    try:
        current_text_ROI = image[start_row:end_row, start_col:end_col]
    except:
        pass

    if((current_text_ROI is None) or (current_text_ROI.shape != result_text.shape)):
        print("No Match: {}".format(file))
        continue
    
    result = reader.readtext(current_text_ROI)

    for detection in result:
        if(detection[1] == "FINAL SCORE"):
            result_posts = open("./results.txt", 'a')
            result_posts.write("{}\n".format(file))
            result_posts.close()

            print(file)

