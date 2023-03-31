'''
Author : MaKaiQiang
dateTime: 2022-11-08
FileName:tushare_handle.py
'''
import time
import undetected_chromedriver as uc
from selenium import webdriver
from stock_app.business.news.page.tushare_news_page import TuSharePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import logging
import json
import cv2
from urllib import request
import pyautogui
import random
from urllib import request
import pytesseract
from PIL import Image
import math
import requests, sys
import ssl
from jsonpath import jsonpath
import base64

pyautogui.FAILSAFE = False
logger = logging.getLogger('django')


def captcha_decode():
    host = 'http://upload.chaojiying.net/Upload/Processing.php'
    with open('captcha.png', 'rb') as f:
        img_content = f.read()
    img = base64.b64encode(img_content)

    data = {
        "user": 'Eros1on',
        "pass": "ma1121624020",
        "softid": 'eb472f29d3a685fd3b859ecac1761004',
        "codetype": '1902',
        "file_base64": img,
    }

    res = requests.post(url=host, json=data, headers={'Content-Type': 'application/json; charset=UTF-8'})
    print(res.text)
    return jsonpath(res.json(), '$..pic_str')[0]


class TuShare():
    def __init__(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.page = TuSharePage(self.driver)
        self.actions = ActionChains(self.driver)

    def login(self):
        self.driver.get('https://tushare.pro/login')
        self.page.user.send_keys('18616386354')
        self.page.password.send_keys('ma1121624020')
        while True:
            captcha_url = self.page.captcha_img.get_attribute('src')
            request.urlretrieve(captcha_url, 'captcha.png')
            result = captcha_decode()
            self.page.captcha.send_keys(result)
            self.page.login.click()
            if self.page.login_info.text == '图形验证码输入错误':
                self.page.captcha.clear()
                continue
            else:
                break

    def get_sina_news(self):
        time.sleep(2)
        self.page.news_data.click()
        self.page.sina_A.click()
        time_ele = self.page.sina_A_news_time.elements()
        content_ele = self.page.sina_A_news_content.elements()
        t = []
        c = []
        for i in time_ele:
            t.append(i.get_attribute('innerHTML'))
        for k in content_ele:
            c.append(k.get_attribute('innerHTML'))
        return {'info': list(zip(t, c)), 'platform': '新浪', 'type': 1}

    def get_east_money_24hour_news(self):
        self.page.east_money.click()
        self.page.east_money_24hour.click()
        time_ele = self.page.east_money_24hour_time.elements()
        content_ele = self.page.east_money_24hour_content.elements()
        t = []
        c = []
        for i in time_ele:
            t.append(i.get_attribute('innerHTML'))
        for k in content_ele:
            c.append(k.get_attribute('innerHTML'))
        return {'info': list(zip(t, c)), 'platform': '东方财富', 'type': 1}

    def get_east_money_important_news(self):
        self.page.east_money_important_news.click()
        time_ele = self.page.east_money_world_time.elements()
        content_ele = self.page.east_money_world_content.elements()
        t = []
        c = []
        for i in time_ele:
            t.append(i.get_attribute('innerHTML'))
        for k in content_ele:
            c.append(k.get_attribute('innerHTML'))
        return {'info': list(zip(t, c)), 'platform': '东方财富', 'type': 2}

    def get_all_platform_news(self):
        self.login()
        sina_news = self.get_sina_news()
        east_money_24 = self.get_east_money_24hour_news()
        east_money_important = self.get_east_money_important_news()
        return [sina_news, east_money_24, east_money_important]


if __name__ == '__main__':
    t = TuShare()
    n = t.get_all_platform_news()
    print(n)
