import os
import glob

def updateFile(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)


filepath="G:\\Fit4CAD-main\\training_set\\"
txt_path=glob.glob(os.path.join(filepath+'*.txt'))
for txt in txt_path:
    updateFile(txt, "[",
               "")  # 将"D:\zdz\"路径的myfile.txt文件把所有的zdz改为daziran
    updateFile(txt, "],", "")
    updateFile(txt, "]", "")
    updateFile(txt, ";", "")
    updateFile(txt, "Points:=", "")
