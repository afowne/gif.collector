import pic_downloader

gif_save_path = 'F:\\gif\\'

t_fanhao = '65.番号：TERA-006  病院隙间淫行为美人妻 芦名尤莉亚'
t_gif='http://ww4.sinaimg.cn/large/006rMPMwgw1f3r7ecdpjqg30b4064u0x.jpg'


dlp = pic_downloader.PicDownloader(Gif_Save_Path=gif_save_path)
max_try_times = 3
current_try_times = 0
while current_try_times < max_try_times:
   if dlp.download_pic_by_request(t_gif,t_fanhao) == 1:
      current_try_times += 1
   else:
      break
if current_try_times==max_try_times:
   dlp.download_pic_by_se(t_gif,t_fanhao)