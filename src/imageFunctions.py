from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
import requests
import os
from selenium import webdriver
from tqdm import tqdm #thư viện hiện tiến trình tải
from bs4 import BeautifulSoup as bs
from tkinter import filedialog
import time
PATH = "data/Chromedriver/chromedriver.exe"

def getHtml(url):   # get link ảnh vào urls = []
    if len(url) == 0:
        messagebox.showerror('Error', 'Bạn chưa nhập URL!')
    else:
        print(url)
        urls = []
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)
            for i in range(70):
                totalScrolledHeight = driver.execute_script("return window.pageYOffset + window.innerHeight")
                height = int(driver.execute_script("return document.documentElement.scrollHeight"))
                if totalScrolledHeight == height:
                    break
                driver.execute_script('window.scrollBy(0, 600)')
                time.sleep(0.1)
            # the script above for auto scroll in order to display all items which are written by js
            html = driver.page_source
            driver.close()
            soup = bs(html, 'lxml')

            for item in soup.findAll('img', {'src' : True}):
                if item is not None:
                    if item['src'].startswith('http'):
                        urls.append(item['src'])
            return urls     
        except:
            return None


def download(url, pathname):    #tải file ảnh với url vừa lấy được và đặt vào thư mục tự đặt tên
    if not os.path.isdir(pathname): # nếu không có directory của folder thì tạo
        os.makedirs(pathname)
    response = requests.get(url, stream=True)   # tải lần lượt theo từng url
    file_size = int(response.headers.get("Content-Length", 0))  # lấy dung lượng ảnh
    filename = os.path.join(pathname, url.split("/")[-1])   # lấy tên file ảnh
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024) # thanh tiến độ tải, chuyển về bytes thay vì iteration (mặc định trong thư viện tqdm)
    files = os.listdir(pathname)
    ext = url[url.rindex('.'):]
    if ext.startswith('.png'):
        ext = '.png'
    elif ext.startswith('.jpg'):
        ext = '.jpg'
    elif ext.startswith('.jfif'):
        ext = '.jfif'
    elif ext.startswith('.com'):
        ext = '.jpg'
    elif ext.startswith('.svg'):
        ext = '.svg'
    with open(f'{pathname}/image{len(files)}{ext}', "wb") as f:
        for data in progress.iterable:
            f.write(data)   # chuyền dữ liệu đọc được vào file
            progress.update(len(data))  # cập nhật tiến độ tải

def getImage(url, path, limit):
    imgs = getHtml(url)  # lấy url ảnh
    if imgs == None:
        return None
    else:        
        cnt = 0
        with ThreadPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
            for img in imgs:
                try:
                    cnt += 1
                    if cnt > limit:
                        break
                    executor.submit(download, *[img, path])
                except:
                    pass
def showFolder():
    filedialog.askopenfile(initialdir="./data/downloadedImages",title="Select a File",filetypes=(("jpg files","*.jpg"),
                                                                                            ('jfif files', '*.jfif'),
                                                                                            ("png files", "*.png"), 
                                                                                            ('svg files', '*.svg'), 
                                                                                            ("all files","*.*")))
       
