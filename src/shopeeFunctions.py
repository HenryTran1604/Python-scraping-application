from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from Product import Product
import os

PATH = 'data/Chromedriver/chromedriver.exe'

def login():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless') #Run in headless mode, i.e., without a UI or display server dependencies. 
    options.add_argument('--disable-notifications')#Disables the Web Notification and the Push APIs.
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=PATH, options=options)
    driver.get("https://shopee.vn/buyer/login")

    # Tìm và điền thông tin đăng nhập (sửa thành tài khoản và mật khẩu của bạn)
    username_input = driver.find_element("name", "loginKey")
    username_input.send_keys("your_username_here")

    password_input = driver.find_element("name", "password")
    password_input.send_keys("your_password_here")
    
    # Submit form đăng nhập
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)
    return driver

def generateLinks(numberOfPage, searched_product):
    urlList = []
    for i in range(numberOfPage):
        search = searched_product.lower().replace(' ', '%20')
        url = "https://shopee.vn/search?keyword={}&page={}".format(search, i)
        urlList.append(url)
    return urlList

def getHtml(driver, url):  # get source code of web
    try:
        driver.get(url)
        time.sleep(3)
        for i in range(15):
            driver.execute_script("window.scrollBy(0, 450)")
            time.sleep(0.1)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        return soup
    except:
        return None

def fillProductList(root, driver, url):
    soup = getHtml(driver, url)
    print(soup)
    if soup == None:
        return
    items = soup.find_all('div', class_='col-xs-2-4 shopee-search-item-result__item')
    for item in items:

        # name
        nameItem = item.find('div', class_='ie3A+n bM+7UW Cve6sh').text
        price = item.findAll('span', class_='ZEgDH9')

        minPrice, maxPrice = 0, 0
        if len(price) > 1:
            minPrice, maxPrice = [int(x.text.replace('.', '')) for x in price]
        else:
            minPrice = maxPrice = int(price[0].text.replace('.', ''))

        # rating
        stars = item.findAll('div', class_='shopee-rating-stars__lit')
        rating = None
        if len(stars) != 0:
            rating = 0
            for star in stars:
                rating += float(star['style'].split()[1][:-2]) / 100

        quantity, sales = item.find('div', class_='r6HknA uEPGHT'), '0'
        if quantity != None:
            sales = quantity.text.split(
            )[-1].replace(',', '').replace('k', '000')

        # link
        linkItem = 'https://shopee.vn' + item.find('a')['href']
        discount_tmp = item.find('span', class_='percent')
        if discount_tmp == None:
            discount = None
        else:
            discount = int(discount_tmp.text[:-1])
        p = Product(nameItem, minPrice, maxPrice, rating, sales, linkItem, discount)
        print(p)
        root.productList.append(p)
def run(root, numberOfPage, searched_product):
    root.productList.clear()
    driver = login()
    urls = generateLinks(numberOfPage, searched_product)
    for url in urls:
        fillProductList(root, driver, url)
    driver.close()

def writeToFile(name, root):
    if len(name) == 0:
        messagebox.showerror("Error", "Bạn chưa nhập tên file")
    else:
        path = './data/shopee'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        csvFile = open(f'{path}/{name}.csv', 'w+',
                       encoding='utf-16', newline='')
        try:
            writer = csv.writer(csvFile, delimiter='\t')
            writer.writerow(
                ('Tên sản phẩm', 'Giá nhỏ nhất', 'Giá lớn nhất', 'Đánh giá sản phẩm', 'Doanh số', 'Giảm giá (%)', 'Link sản phẩm'))
            writer.writerows(root.productList)
        except:
            messagebox.showerror('ERROR', 'Đã có lỗi xảy ra!')
        finally:
            csvFile.close()
            messagebox.showinfo(
                "Sucessfully!", 'Đã lưu vào file vào thư mục data')

