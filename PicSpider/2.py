#使用selenium和pyautogui右键保存图片
import os
import pymysql

f = open('aa.txt', 'a')

rootdir = 'E:\gif'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i in range(0,len(list)):
   path = os.path.join(rootdir,list[i])
   if os.path.isfile(path):
         f.write("insert into a_test values ('" +path+"');\n")

f.write("\n")
f.write("\n")
f.write("\n")

conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
cursor=conn.cursor()
cursor.execute("SELECT gif_URL FROM gifdatabase.gif_detail")
data = cursor.fetchall()

for i in data:
   f.write("'" +i[0]+"',\n")

cursor.close()
conn.close()

f.close()