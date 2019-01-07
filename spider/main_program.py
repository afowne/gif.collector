#1.解析
#2.下载
#3.判重
#4.入库

import pic_extracter
import pic_downloader

target = '3347321'
target_path = 'data\\3\\'
gif_save_path = 'F:\\gif\\'


# dlp = pic_downloader.PicDownloader(Gif_Save_Path=gif_save_path)
# dlp.download_pic_from_local('C:\\Users\\afowne\\Desktop\\21251130.gif','DMS-018')

target_tuple= pic_extracter.extract3(target,target_path)
lst_fanhao = target_tuple[0]
lst_gif=target_tuple[1]

dlp = pic_downloader.PicDownloader(Gif_Save_Path=gif_save_path)
for i in range(0, len(lst_fanhao)):
    max_try_times = 3
    current_try_times = 0
    while current_try_times < max_try_times:
        if dlp.download_pic_by_request(lst_gif[i],lst_fanhao[i]) == 1:
            current_try_times += 1
        else:
            break
    if current_try_times==max_try_times:
        dlp.download_pic_by_se(lst_gif[i],lst_fanhao[i])







