import os
import numpy as np
import glob
from PIL import Image
import re

file_path = "E:\\dataset\\test1\\label\\"  # 文件夹路径
file_path1 = "E:\\dataset\\test1\\label2\\"
images_path = glob.glob(os.path.join(file_path + '*.tif'))  # 所有图片路径
for image_path in images_path:
    image=Image.open(image_path)
    pattern = re.compile(r'([^<>/\\\|:""\*\?]+)\.\w+$')
    data = pattern.findall(image_path)
    data_now = data[0]
    name = str(data_now) + ".tif"

    width,height=image.size
    for y in range(height):
        for x in range(width):
            r,g,b=image.getpixel((x,y))
            if r==255 and g==255 and b==255:
                r=255
                g=0
                b=0
            else:
                r=0
                g=0
                b=0
            image.putpixel((x,y),(r,g,b))
    image.save(file_path1+name)