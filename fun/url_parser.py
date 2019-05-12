#!/usr/bin/env python
# coding:utf8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image, ImageEnhance
import pytesseract
import time
import json
from lxml import etree


class UrlParser(object):
    def __init__(self):
        self.service_args = []
        self.phantomjs = 'phantomjs.exe'
        self.chrome = 'chromedriver.exe'
        self.firefox = 'geckodriver.exe'

    def web_driver(self):
        # driver = webdriver.PhantomJS(executable_path=self.phantomjs, service_args=self.service_args)
        driver = webdriver.Chrome(executable_path=self.chrome, service_args=self.service_args)
        # driver = webdriver.Firefox(executable_path=self.firefox)
        driver.maximize_window()
        return driver

    def driver_content(self, url, cookies=None):
        while True:
            try:
                driver = self.web_driver()
                driver.get(url)
                if cookies is not None:
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                driver.refresh()
                time.sleep(1)
                html = driver.page_source
                driver.quit()
                break
            except Exception as e:
                print(url, e.__str__())
                continue
        return html

    @staticmethod
    def soup(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def soup_driver(self, url, cookies=None):
        html = self.driver_content(url, cookies)
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    def soup_request(url, headers=None, cookies=None):
        cookies_dict = dict()
        if cookies is not None:
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
        while True:
            try:
                response = requests.get(url, headers=headers, cookies=cookies_dict)
                soup = BeautifulSoup(response.text, 'html.parser')
                break
            except Exception as e:
                print(e.__str__())
                time.sleep(2)
                continue
        return soup

    def lxml_html(self, html):
        html = etree.HTML(str(html))
        result = etree.tostring(html)
        soup = self.soup(result)
        return soup

    def login(self, url):
        driver = self.web_driver()
        driver.get(url)
        driver.find_element_by_xpath('//*[contains(@id,"username")]').send_keys('isjin')
        driver.find_element_by_xpath('//*[contains(@id,"password")]').send_keys('zaq1@WSX')
        # img_element=driver.find_element_by_xpath('//*[@id="vseccode_cS"]/img')
        time.sleep(30)
        driver.find_elements_by_tag_name('button')[1].click()
        time.sleep(1)
        cookies = driver.get_cookies()
        f = open('cookies.txt', 'w')
        f.write(json.dumps(cookies))
        f.close()
        driver.quit()
        return cookies

    @staticmethod
    def get_auth_code(img_element):
        img_size = img_element.size
        img_location = img_element.location
        print(img_location)
        rangle = (int(img_location['x']), int(img_location['y']), int(img_location['x'] + img_size['width']),
                  int(img_location['y'] + img_size['height']))
        print(rangle)
        login_png = Image.open("login.png")
        enh_bri = ImageEnhance.Brightness(login_png)
        brightness = 2.5
        login_png = enh_bri.enhance(brightness)
        enh_col = ImageEnhance.Color(login_png)
        color = 4
        login_png = enh_col.enhance(color)
        enh_con = ImageEnhance.Contrast(login_png)
        contrast = 2
        login_png = enh_con.enhance(contrast)
        enh_sha = ImageEnhance.Sharpness(login_png)
        sharpness = 4.0
        login_png = enh_sha.enhance(sharpness)
        login_png.show()
        frame4 = login_png.crop(rangle)
        frame4.save('authcode.png')
        authcode_img = Image.open('authcode.png')
        authcode = pytesseract.image_to_string(authcode_img).strip()
        return authcode