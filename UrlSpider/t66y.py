import urllib
from pyquery import PyQuery
import time
import random


def filefind(ftype,title,url):
    f=open('log\\t66y_'+ftype+'.txt', 'r', encoding='UTF-8')
    text = f.read()
    f.close()
    if url.find("3320542")>0 or url.find("3345742")>0 or url.find("3347321")>0 or url.find("3344256")>0 or url.find("3317327")>0 or url.find("3321440")>0:
        return 0
    if text.find(url) ==-1:
        with open('log\\t66y_'+ftype+'.txt','a', encoding='UTF-8') as ff:
            ff.write(title+"  ----------  https://t66y.com/"+ url+"\n")
        return 1


try:
    for m in range(61,101):
        print(str(m))
        url='https://t66y.com/thread0806.php?fid=7&search=&page='+str(m)
        header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
        }
        request = urllib.request.Request(url, headers=header)
        reponse = urllib.request.urlopen(request).read()
        doc = PyQuery(reponse)

        for i in range(3,103):
            selector ='#ajaxtable > tbody:nth-child(2) > tr:nth-child('+str(i)+') > td.tal > h3 > a'
            p = doc(selector)
            if p.length == 0:
                continue
            ptext =str(p.text()).lower()

            if ptext.find("gif") >-1:
                filefind('gif',str(p.text()),str(p.attr.href))
            elif ptext.find("动图") >-1:
                filefind('动图',str(p.text()),str(p.attr.href))
        time.sleep(int(random.uniform(305,325)))
except Exception as e:
    print(str(e))
