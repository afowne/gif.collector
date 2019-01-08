import re

fo= open("F:\\gif\\2222.txt", 'r', encoding='UTF-8')

lst_filted=[]
for line in fo:
    bangou = line.split("||")
    b = bangou[0].replace("：",":").split("番号:")[1].replace(" ","").replace("?","")

    #pattern1 = re.compile(r"([a-zA-Z]{1,4})(-|00|_|)([0-9]{3})((-|_|)[CcRr]){0,}")
    pattern1 = re.compile(r"[A-Za-z]+-[0-9]+")#一般情况
    b1 = re.findall(pattern1,b)

    if(len(b1)>0):
        lst_filted.append(''.join(b1))
    else:
        pattern2 = re.compile('[A-Za-z]{2,}[0-9]{2,}')#没有-的情况
        b2 = re.findall(pattern2,b)
        if(len(b2)>0):
            lst_filted.append(''.join(b2))
        else:
            pattern3 = re.compile('[0-9]{2,}-[0-9]{3,}') #加勒比
            b3 = re.findall(pattern3,b)
            if(len(b3)>0):
                lst_filted.append(''.join(b3))
            else:
                pattern4 = re.compile('[A-Za-z]{2,}-[A-Za-z0-9,，]{3,}') #CRS-S014
                b4 = re.findall(pattern4,b)
                if(len(b4)>0):
                    lst_filted.append(''.join(b4))
                else:
                    pattern5 = re.compile('[A-Za-z0-9.]+')
                    b5 = re.findall(pattern5,b)
                    if(len(b5)>0):
                        print(''.join(b5))

# for i in lst_filted:
#     print( i)




