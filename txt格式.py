#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import glob
import re


# oldfile:UTF8文件的路径
# newfile:要保存的ANSI文件的路径
def convertUTF8ToANSI(oldfile, newfile):
    f = codecs.open(oldfile, 'r', 'utf8')
    utfstr = f.read()
    f.close()

    # 把UTF8字符串转码成ANSI字符串
    outansestr = utfstr.encode('mbcs')

    # 使用二进制格式保存转码后的文本
    f = open(newfile, 'wb')
    f.write(outansestr)
    f.close()

filepath1="C:\\Users\\LHB\\Desktop\\1\\"
filepath2="C:\\Users\\LHB\\Desktop\\2\\"
txt_path=glob.glob(os.path.join(filepath1+'*.txt'))
for txt in txt_path:
    pattern=re.compile(r'([^<>/\\\|:""\*\?]+)\.\w+$')
    data=pattern.findall(txt)
    data_=data[0]
    name=str(data_)+".txt"
    convertUTF8ToANSI(txt,filepath2+name)