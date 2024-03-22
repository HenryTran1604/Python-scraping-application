from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
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

    time.sleep(2)

    # Tìm và điền thông tin đăng nhập (sửa thành tài khoản và mật khẩu của bạn)
    username_input = driver.find_element("name", "loginKey")
    username_input.send_keys("0904845743")

    password_input = driver.find_element("name", "password")
    password_input.send_keys("387420489Huy")

    # Submit form đăng nhập
    password_input.send_keys(Keys.ENTER)

    # Đợi một thời gian sau khi đăng nhập trước khi truy cập trang chính
    time.sleep(3)
login()