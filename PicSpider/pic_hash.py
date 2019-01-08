import imagehash
import pymysql
from PIL import Image
import pic_split
import banngou
import math
import os
import pic_log

def handle_pic(pic_path,pic_title,source_URL):
    lst_frame = pic_split.ImageSpliter(pic_path)
    #帧数只有1
    if len(lst_frame) == 1 or len(lst_frame) == 0:
        os.remove(pic_path)
        pic_log.log_print("非动态图： %s||%s" % (pic_title,source_URL))
        return 2

    try:
        #将gif的每帧Image构建一个数组
        lst_phash=[]
        for frame in lst_frame:
            lst_phash.append(imagehash.phash(frame))
        #去除第一帧
        lst_phash.pop(0)
        #保存第二帧作为标准帧
        phash_standard = lst_phash[0]
        #去除重复帧
        lst_phash = list(set(lst_phash))
        if(len(lst_phash)>0):
            #计算汉明距离并存入字典，其中hash为key，距离为value
            dict_phash = {}
            for i in range(0,len(lst_phash)):
                dict_phash[lst_phash[i]] = lst_phash[i]-phash_standard
            #按照value从大到小排序
            dict_phash= sorted(dict_phash.items(), key=lambda d:d[1], reverse = True)
            #待优化
            #取三个fp作为样本，第一个，和第一个相差最大的，和处于中间的
            goto_insert_phash =[]
            goto_insert_phash.append(phash_standard)
            goto_insert_phash.append(dict_phash[0][0])
            goto_insert_phash.append(dict_phash[(math.floor(len(dict_phash)/2))][0])
            goto_insert_phash = list(set(goto_insert_phash))
    except Exception as e:
        pic_log.log_print("handle_pic出错： %s (输入参数：pic_path[%s];pic_title[%s];source_URL:[%s])" % (str(e),pic_path,pic_title,source_URL))
        return 6
    
    #待优化
    #寻找样本fp有没有相同的
    gif_ID = None
    for i in goto_insert_phash:
        gif_ID=find_fingerprint_by_fp(str(i))
        if gif_ID!=None:
            break
    #有相同的删除下载文件并结束本次录入
    if gif_ID != None:
        os.remove(pic_path)
        pic_log.log_print("重复样本： %s||%s" % (pic_title,source_URL))
        return 2
    #提取番号并记录
    _banngou = banngou.filter_it(pic_title)
    if _banngou == "":
        pic_log.log_print("空白标题： %s||%s" % (pic_title,source_URL))
        return 3
    banngou_ID = banngou.find_banngou_id(_banngou)
    if banngou_ID == None:
        pic_log.log_print("番号获取失败： %s||%s" % (pic_title,source_URL))
        return 4
    #插入新的gif_detail
    gif_ID =add_gif_detail(pic_path,banngou_ID,pic_title,source_URL)
    if gif_ID == None:
        return 5
    #插入三个新的fp样本
    for i in goto_insert_phash:
        add_fingerprint(i,gif_ID,bin(int(str(i),16))[2:])
    return 0

def search_pic_by_path(pic_path):
    lst_frame = pic_split.ImageSpliter(pic_path)
    #帧数只有1
    if len(lst_frame) == 1 or len(lst_frame) == 0:
        os.remove(pic_path)
        pic_log.log_print("非动态图： %s||%s" % ('',''))
        return 2

    try:
        #将gif的每帧Image构建一个数组
        lst_phash=[]
        for frame in lst_frame:
            lst_phash.append(imagehash.phash(frame))
        #去除第一帧
        lst_phash.pop(0)
        #保存第二帧作为标准帧
        phash_standard = lst_phash[0]
        #去除重复帧
        lst_phash = list(set(lst_phash))
        if(len(lst_phash)>0):
            #计算汉明距离并存入字典，其中hash为key，距离为value
            dict_phash = {}
            for i in range(0,len(lst_phash)):
                dict_phash[lst_phash[i]] = lst_phash[i]-phash_standard
            #按照value从大到小排序
            dict_phash= sorted(dict_phash.items(), key=lambda d:d[1], reverse = True)
            #待优化
            #取三个fp作为样本，第一个，和第一个相差最大的，和处于中间的
            goto_insert_phash =[]
            goto_insert_phash.append(phash_standard)
            goto_insert_phash.append(dict_phash[0][0])
            goto_insert_phash.append(dict_phash[(math.floor(len(dict_phash)/2))][0])
            goto_insert_phash = list(set(goto_insert_phash))
    except Exception as e:
        return 6
    
    #待优化
    #寻找样本fp有没有相同的
    gif_ID = None
    for i in goto_insert_phash:
        gif_ID=find_fingerprint_by_fp(str(i))
        if gif_ID!=None:
            break
    #有相同的删除下载文件并结束本次录入
    if gif_ID != None:
        os.remove(pic_path)
        pic_log.log_print("重复样本： %s||%s" % ('',''))
        return 2
    #提取番号并记录
    _banngou = banngou.filter_it(pic_title)
    if _banngou == "":
        pic_log.log_print("空白标题： %s||%s" % ('',''))
        return 3
    banngou_ID = banngou.find_banngou_id(_banngou)
    if banngou_ID == None:
        pic_log.log_print("番号获取失败： %s||%s" % ('',''))
        return 4
    return 0

def add_gif_detail(gif_URL,banngou_ID,source_title,source_URL):
    ret = None
    try:
        conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
        cursor=conn.cursor()
        sql = "INSERT INTO gif_detail(`gif_URL`,`banngou_ID`,`source_title`,`source_URL`) VALUES ('"+gif_URL.replace('\\','\\\\')+"','"+str(banngou_ID)+"','"+source_title+"','"+source_URL+"')"
        cursor.execute(sql)
        ret = conn.insert_id()
        conn.commit()
    except Exception as e:
        pic_log.log_print("add_gif_detail出错： %s (gif_URL[%s];banngou_ID[%s];source_title:[%s];source_URL:[%s])" % (str(e),gif_URL,banngou_ID,source_title,source_URL))
    finally:
        cursor.close()
        conn.close()
        return ret
    

def add_fingerprint(fingerprint,gif_ID,fp_bin):
    ret = None
    try:
        conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
        cursor=conn.cursor()
        sql = "INSERT INTO fingerprint(`fingerprint`,`gif_ID`,`fp_bin`) VALUES ('"+str(fingerprint)+"','"+str(gif_ID)+"','"+fp_bin+"')"
        cursor.execute(sql)
        ret = conn.insert_id()
        conn.commit()
    except Exception as e:
        pic_log.log_print("add_fingerprint出错： %s (输入参数：fingerprint[%s];gif_ID[%s];fp_bin:[%s])" % (str(e),fingerprint,gif_ID,fp_bin))
    finally:
        cursor.close()
        conn.close()
        return ret
    

def find_fingerprint_by_fp(fingerprint):
    ret = None
    try:
        conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
        cursor=conn.cursor()
        cursor.execute("select gif_ID from fingerprint where fingerprint='"+fingerprint+"'")
        data = cursor.fetchone()
        if(data != None):
            ret = data[0]
    except Exception as e:
        pic_log.log_print("find_fingerprint_by_fp出错： %s (输入参数：fingerprint[%s])" % (str(e),fingerprint))
    finally:
        cursor.close()
        conn.close()
        return ret 
    

def load_all_fp():
    conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
    cursor=conn.cursor()  
    cursor.execute("select ID,fingerprint,fp_bin from fingerprint")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return data


#search_pic_by_path('E:\\gif\\1546871949016.gif')

#handle_pic('F:\gif\qq.gif','ssss')

#find_fingerprint_by_fp('cf7d33498981e18b')


# for i in range(0,3):
#     print(bin(int(str(dict_phash[i][0]),16))[2:])
#     conn = pymysql.connect(host='118.24.86.12',user='root',passwd='aries0327',db='gifdatabase',port=3306)
#     cursor=conn.cursor()
#     sql = "INSERT INTO fingerprint(`fingerprint`,`gif_ID`,`fp_bin`) VALUES ('"+str(dict_phash[i][0])+"',0,'"+bin(int(str(dict_phash[i][0]),16))[2:]+"')"
#     cursor.execute(sql)
#     ret = conn.insert_id()
#     conn.commit()
#     cursor.close()
#     conn.close()