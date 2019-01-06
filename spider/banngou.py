import re
import pymysql
import pic_log

def find_banngou_id(banngou):
    ret = None
    try:
        conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
        cursor=conn.cursor()
        cursor.execute("select banngou_ID from banngou_detail where banngou='"+banngou+"'")
        data = cursor.fetchone()

        if(data == None):
            sql = "INSERT INTO banngou_detail(`banngou_ID`,`banngou`) VALUES ('0', '"+banngou+"')"
            cursor.execute(sql)
            ret = conn.insert_id()
            conn.commit()
        else:
            ret = int(data[0])
    except Exception as e:
        pic_log.log_print("find_banngou_id出错： %s (输入参数：banngou[%s])" % (str(e),banngou))
    finally:
        cursor.close()
        conn.close()
        return ret


def filter_it(content):
    lst_filted = []
    try:
        b = content.replace("：",":").split("番号:")
        if len(b)>1:
            b=b[1]
        else:
            b=b[0]
        b=b.replace(" ","").replace("?","")

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
                        lst_filted.append(b)
    except Exception as e:
        pic_log.log_print("filter_it出错： %s (输入参数：content[%s])" % (str(e),content))
        lst_filted.append("")
    finally:
        return lst_filted[0]
