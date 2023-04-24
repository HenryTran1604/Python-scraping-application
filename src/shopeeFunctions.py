from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
from Product import Product
import os

PATH = 'data/Chromedriver/chromedriver.exe'

def generateLinks(numberOfPage, searched_product):
    urlList = []
    for i in range(numberOfPage):
        search = searched_product.lower().replace(' ', '%20')
        url = "https://shopee.vn/search?keyword={}&page={}".format(search, i)
        urlList.append(url)
    return urlList

def getHtml(url):  # get source code of web
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=PATH, options=options)
        driver.get(url)
        time.sleep(3)
        for i in range(15):
            driver.execute_script("window.scrollBy(0, 450)")
            time.sleep(0.1)
        
        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html, 'lxml')
        return soup
    except :
        return None

def fillProductList(root, url):
    soup = getHtml(url)
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
        rating = 0
        if stars != None:
            for star in stars:
                rating += float(star['style'].split()[1][:-2]) / 100

        quantity, sales = item.find('div', class_='r6HknA uEPGHT'), '0'
        if quantity != None:
            sales = quantity.text.split(
            )[-1].replace(',', '').replace('k', '000')

        # link
        linkItem = 'https://shopee.vn' + item.find('a')['href']
        p = Product(nameItem, minPrice, maxPrice, rating, sales, linkItem)
        root.productList.append(p)
def run(root, numberOfPage, searched_product):
    root.productList.clear()
    urls = generateLinks(numberOfPage, searched_product)
    with ThreadPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
        for url in urls:
            executor.submit(fillProductList, *[root, url])

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
                ('Tên sản phẩm', 'Giá nhỏ nhất', 'Giá lớn nhất', 'Đánh giá sản phẩm', 'Doanh số', 'Link sản phẩm'))
            writer.writerows(root.productList)
        except:
            messagebox.showerror('ERROR', 'Đã có lỗi xảy ra!')
        finally:
            csvFile.close()
            messagebox.showinfo(
                "Sucessfully!", 'Đã lưu vào file vào thư mục data')

