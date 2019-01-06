from pyquery import PyQuery


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