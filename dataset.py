import os
from osgeo import gdal
import numpy as np
import glob

#  读取tif数据集
def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "文件无法打开")
    return dataset


#  保存tif文件函数
def writeTiff(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


def TifCrop(TifPath, SavePath, CropSize, RepetitionRate):
    dataset_img = readTif(TifPath)
    width = dataset_img.RasterXSize
    height = dataset_img.RasterYSize
    proj = dataset_img.GetProjection()
    geotrans = dataset_img.GetGeoTransform()
    img = dataset_img.ReadAsArray(0, 0, width, height)  # 获取数据

    #  获取当前文件夹的文件个数len,并以len+1命名即将裁剪得到的图像
    new_name = len(os.listdir(SavePath)) + 1
    #  裁剪图片,重复率为RepetitionRate

    for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
        for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
            #  如果图像是单波段
            if (len(img.shape) == 2):
                cropped = img[
                          int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                          int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
            #  如果图像是多波段
            else:
                cropped = img[:,
                          int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                          int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
            #  写图像
            writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
            #  文件名 + 1
            new_name = new_name + 1
    #  向前裁剪最后一列
    for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
        if (len(img.shape) == 2):
            cropped = img[int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                      (width - CropSize): width]
        else:
            cropped = img[:,
                      int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                      (width - CropSize): width]
        #  写图像
        writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
        new_name = new_name + 1
    #  向前裁剪最后一行
    for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
        if (len(img.shape) == 2):
            cropped = img[(height - CropSize): height,
                      int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
        else:
            cropped = img[:,
                      (height - CropSize): height,
                      int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
        writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
        #  文件名 + 1
        new_name = new_name + 1
    #  裁剪右下角
    if (len(img.shape) == 2):
        cropped = img[(height - CropSize): height,
                  (width - CropSize): width]
    else:
        cropped = img[:,
                  (height - CropSize): height,
                  (width - CropSize): width]
    writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
    new_name = new_name + 1


#  将影像1裁剪为重复率为0.1的256×256的数据集

file_path1 = "E:\\dataset\\test1\\image\\"  # 文件夹路径
images_path = glob.glob(os.path.join(file_path1 + '*.tif'))  # 所有图片路径
for image_path in images_path:
    #image = cv2.imread(image_path)
    TifCrop(image_path,r"E:\\dataset\\test1\\image1", 512, 0.5)
file_path2 = "E:\\dataset\\test1\\label\\"  # 文件夹路径
labels_path = glob.glob(os.path.join(file_path2 + '*.tif'))  # 所有图片路径
for label_path in labels_path:
    #image = cv2.imread(image_path)
    TifCrop(label_path, r"E:\\dataset\\test1\\label1", 512, 0.5)