#!/usr/bin/env python
# coding:utf8
import os


class UrlManager(object):
    def __init__(self):
        # self.super_folder=os.path.abspath(os.path.dirname(os.getcwd()))
        # self.program_file = 'url/programs.txt'
        # self.videos_file = 'url/videos.txt'
        self.failed_urls_file = 'url/failed_urls.txt'
        self.old_iguxuan_urls_file = 'url/old_iguxuan_urls.txt'
        self.old_yzb_urls_file = 'url/old_yizhibo_urls.txt'
        # self.related_info_file = 'url/related_info.txt'
        # self.programs_info = self.read_file(self.program_file)
        self.old_iguxuan_urls = set()
        self.old_yzb_urls = set()
        self.failed_urls = set()
        self.initial_old_iguxuan_urls()
        self.initial_old_yzb_urls()
        self.initial_failed_urls()

    # def initial_videos(self):
    #     if os.path.exists(self.videos_file):
    #         open(self.videos_file, 'w')

    @staticmethod
    def read_file(file_path):
        info = []
        f = open(file_path, 'r', encoding='utf8')
        # f = open(file_path, 'r')
        lines = f.readlines()
        for line in lines:
            info.append(str(line).strip())
        return info

    def initial_old_iguxuan_urls(self):
        file = self.old_iguxuan_urls_file
        if os.path.exists(file):
            data = self.read_file(file)
            for i in data:
                self.old_iguxuan_urls.add(i)

    def initial_old_yzb_urls(self):
        file = self.old_yzb_urls_file
        if os.path.exists(file):
            data = self.read_file(file)
            for i in data:
                self.old_yzb_urls.add(i)

    def initial_failed_urls(self):
        file = self.failed_urls_file
        if os.path.exists(file):
            data = self.read_file(file)
            for i in data:
                self.failed_urls.add(i)

    def add_parse_failed_url(self, video_url):
        if video_url not in self.failed_urls:
            self.write_file(video_url, self.failed_urls_file)
            self.failed_urls.add(video_url)

    def add_old_yzb_urls(self, video_url):
        if video_url not in self.old_yzb_urls:
            self.write_file(video_url, self.old_yzb_urls_file)
            self.old_yzb_urls.add(video_url)

    def add_old_iguxuan_urls(self, video_url):
        if video_url not in self.old_iguxuan_urls:
            self.write_file(video_url, self.old_iguxuan_urls_file)
            self.old_iguxuan_urls.add(video_url)

    # def add_related_info(self, info):
    #     self.write_file(info, self.related_info_file)

    def write_file(self, url_info, file_path):
        f = open(file_path, 'a+', encoding='utf8')
        if isinstance(url_info, str):
            while True:
                try:
                    f.write(url_info + '\n')
                    break
                except Exception as e:
                    print(e.__str__())
        else:
            for i in url_info:
                while True:
                    try:
                        f.write(i + '\n')
                        break
                    except Exception as e:
                        print(e.__str__())
        f.close()


if __name__ == '__main__':
    app = UrlManager()
