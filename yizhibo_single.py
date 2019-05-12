#!/usr/bin/env python
# coding:utf8
from fun.url_parser import UrlParser
from fun.url_manager import UrlManager
from fun.downloader import DownLoader
from multiprocessing import Pool
import re


class YiZhiBo(object):
    def __init__(self):
        self.urlparser = UrlParser()
        self.urlmanager = UrlManager()
        self.downloader = DownLoader()
        self.yzb_video_url = 'yzb_video_url.txt'

    def get_urls(self):
        urls = []
        f = open(self.yzb_video_url, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            urls.append(str(line).strip())
        return urls

    def get_video_m3u8(self, video_url):
        print(video_url)
        html = self.urlparser.soup_request(video_url)
        m3u8_url = html.find('video').get('src')
        date_p = html.find_all('p')[-1]
        date = re.search(r'\d+-\d+-\d+', str(date_p)).group()
        date = str(date).replace('-', '')
        return m3u8_url, date

    def yizhibo_single_download(self, video_url, title):
        video_url_m3u8, date = self.get_video_m3u8(video_url)
        filename = date + '-' + title
        self.downloader.download_mp4_single(video_url_m3u8, filename)
        self.urlmanager.add_old_yzb_urls(video_url)
        return

    def run(self, video_url):
        html = self.urlparser.soup_request(video_url)
        title = html.find_all('meta')[2].get('content')
        title = re.sub(r'>>', '', str(title))
        # print(html.find_all('div'))
        self.yizhibo_single_download(video_url, title)


if __name__ == '__main__':
    app = YiZhiBo()
    p = Pool()
    for url in app.get_urls():
        app.run(url)
        # p.apply_async(app.run, (url,))
    p.close()
    p.join()
