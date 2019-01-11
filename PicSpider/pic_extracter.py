from pyquery import PyQuery

#先番号再图片
#175.番号：APAA-264
def extract(target,target_path):
    with open(target_path +target+".txt", 'r', encoding='UTF-8') as htmlfile:
        text = htmlfile.read()
        doc = PyQuery(text)

    lst_fanhao = []
    lst_gif = []
    for i in doc.children():
        if(len(lst_fanhao) == len(lst_gif)):
            if i.tag == "br":
                if i.tail != None and (i.tail.find('番号：') >= 0 or i.tail.find('番号:') >= 0):
                    lst_fanhao.append(i.tail)
                    continue
        if(len(lst_fanhao) > len(lst_gif)):
            if i.tag == "img":
                lst_gif.append(i.attrib["src"])
    return (lst_fanhao,lst_gif)

#先番号再图片
#GAR-374
def extract2(target,target_path):
    with open(target_path +target+".txt", 'r', encoding='UTF-8') as htmlfile:
        text = htmlfile.read()
        doc = PyQuery(text)

    lst_fanhao = []
    lst_gif = []
    last_fanhao = ""
    for i in doc.children():
        if(len(lst_fanhao) == len(lst_gif)):
            if i.tag == "br":
                if i.tail != None and i.tail != '\n':
                    lst_fanhao.append(i.tail)
                    last_fanhao = i.tail
                    continue
        if i.tag == "img":  
            if(len(lst_fanhao) == len(lst_gif)):
                lst_fanhao.append(last_fanhao)
            lst_gif.append(i.attrib["src"])
    return (lst_fanhao,lst_gif)

#先图片再番号
#GAR-374
def extract3(target,target_path):
    with open(target_path +target+".txt", 'r', encoding='UTF-8') as htmlfile:
        text = htmlfile.read()
        doc = PyQuery(text)

    lst_fanhao = []
    lst_gif = []
    for i in doc.children():
        if(len(lst_gif) == len(lst_fanhao)):
            if i.tag == "img":
                lst_gif.append(i.attrib["src"])
        if(len(lst_gif) > len(lst_fanhao)):
            if i.tag == "br":
                if i.tail != None and i.tail != '\n':
                    lst_fanhao.append(i.tail)
                    continue
            
    return (lst_fanhao,lst_gif)