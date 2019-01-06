#使用selenium和pyautogui右键保存图片
import os

rootdir = 'F:\gif'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i in range(0,len(list)):
   path = os.path.join(rootdir,list[i])
   if os.path.isfile(path):
      print(path)

