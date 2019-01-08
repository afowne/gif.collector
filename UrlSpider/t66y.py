import urllib
import requests
from pyquery import PyQuery


def filefind(ftype,title,url):
    f=open('log\\t66y_'+ftype+'.txt', 'r', encoding='UTF-8')
    text = f.read()
    f.close()
    if text.find(url) ==-1:
        with open('log\\t66y_'+ftype+'.txt','a', encoding='UTF-8') as ff:
            ff.write(title+"  ----------  https://t66y.com/"+ url+"\n")


for m in range(1,101):
    url='https://t66y.com/thread0806.php?fid=7&search=&page='+str(m)
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
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


