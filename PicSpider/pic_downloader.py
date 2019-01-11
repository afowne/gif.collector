import urllib

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import shutil
import os

import time
import pic_log
import pic_hash


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Accept-Language': 'zh-CN',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'Keep-Alive',
    'Pragma': 'no-cache'
}

class PicDownloader:
    _gif_save_path = ""
    _se_source_path = ""
    _filename = ""
    _filepath = ""
    def __init__(self,Gif_Save_Path,Se_source_path):
        self._gif_save_path=Gif_Save_Path
        self._se_source_path=Se_source_path

    def download_pic_by_request(self,d_url, d_title):
        ret = 1
        try:
            self._generate_file_name()

            req = urllib.request.Request(d_url, headers=header)
            data = urllib.request.urlopen(req, timeout=10).read()
            
            if(not self._check_file_size(len(data))):
                ret = 2
            else:
                with open(self._filepath, 'wb') as f:
                    f.write(data)
                    f.close()
                ret = pic_hash.handle_pic(self._filepath,d_title,d_url)
                #pic_log.log_print("download_pic_by_request成功： %s (%s)" % (self._filepath,d_title))
        except Exception as e:
            #pic_log.log_print("download_pic_by_request出错： %s (d_url[%s],d_title[%s])" % (str(e),d_url,d_title))
            pass
        finally:
            return ret

    def download_pic_by_se(self,d_url, d_title):
        ret = 1
        try:
            self._generate_file_name()
        
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {
            "download.default_directory": self._gif_save_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })

            driver = webdriver.Chrome(chrome_options=options)
            driver.get(d_url)
            driver.implicitly_wait(50)
            gaikuang = driver.find_element_by_xpath("/html/body/img")
            action = ActionChains(driver).move_to_element(gaikuang)  # 移动到该元素
            action.context_click(gaikuang)  # 右键点击该元素
            action.perform()  # 执行保存
            pyautogui.typewrite(['v'])
            time.sleep(1)
            pyautogui.typewrite(self._filename, 0.1)
            pyautogui.typewrite(['enter'])
            pyautogui.typewrite(['enter'])
            time.sleep(1)

            if(not self._check_file_size(os.path.getsize(self._se_source_path+self._filename))):
                os.remove(self._se_source_path+self._filename)
                ret = 2
            else:
                shutil.move(self._se_source_path+self._filename,self._filepath)

                ret = pic_hash.handle_pic(self._filepath,d_title,d_url)
                #pic_log.log_print("download_pic_by_se成功： %s (%s)" % (self._filepath,d_title))
        except Exception as e:
            pic_log.log_print("download_pic_by_se出错： %s (d_url[%s],d_title[%s])" % (str(e),d_url,d_title))
        finally:
            driver.close()
            return ret

    def download_pic_from_local(self,d_url,d_title):
        try:
            self._generate_file_name()
            shutil.move(d_url,self._filepath)
            pic_hash.handle_pic(self._filepath,d_title,'local')
        except Exception as e:
            pass


    def _generate_file_name(self):
        self._filename = str(int(round(time.time() * 1000)))+".gif"
        self._filepath = self._gif_save_path + self._filename

    def _check_file_size(self,datalen):
        if (datalen>102400):
            return True
        else:
            return False


def log_print(content):
    logging.info(content)
    print(content)
