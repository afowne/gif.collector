import os
from PIL import Image
import pic_log

def analyseImage(path):
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results
 
def ImageSpliter(path):
    lst_frame=[]
    try:
        mode = analyseImage(path)['mode']
        im = Image.open(path)
        
        i = 0
        p = im.getpalette()
        last_frame = im.convert('RGBA')
        while True:
            if not im.getpalette():
                im.putpalette(p)
            
            new_frame = Image.new('RGBA', im.size)
            if mode == 'partial':
                new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            lst_frame.append(new_frame)
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except Exception as e:
        #pic_log.log_print("ImageSpliter出错： %s (path[%s])" % (str(e),path))
        pass
    finally:
        return lst_frame
 