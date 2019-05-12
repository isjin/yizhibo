#!/usr/bin/env python
# coding:utf8
import os
import shutil
import requests
import re


def check_file_size(path):
    size = os.path.getsize(path)
    if size < 8000:
        os.remove(path)
    return


class DownLoader(object):
    @staticmethod
    def createfloder(floder):
        if os.path.exists('./video/%s' % floder):
            pass
        else:
            os.mkdir('./video/%s' % floder)
        return

    @staticmethod
    def create_subfloder(teacher, folder):
        if os.path.exists('./video/%s/%s' % (teacher, folder)):
            pass
        else:
            os.mkdir('./video/%s/%s' % (teacher, folder))
        return

    @staticmethod
    def create_date_floder(path):
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        return

    def download_mp4(self, url, path, filename):
        print(url)
        media_name = './temp/' + str(filename) + '.mp4'
        download_response = requests.get(url, stream=True)
        open_path = path + str(filename) + '.mp4'
        open_path = self.existed_file(open_path)
        f = open(media_name, 'wb')
        for chunk in download_response.iter_content(chunk_size=512 * 1024):
            if chunk:
                f.write(chunk)
        f.close()
        download_response.close()
        # check_file_size(media_name)
        # if os.path.exists(media_name) is True:
        #     # shutil.move(media_name, open_path)
        #     self.compress_video(media_name, open_path)
        #     os.remove(media_name)
        return

    # def compress_video(self, source_file, dest_file):
    #     dest_temp_file = re.sub(r'temp', 'temp2', str(source_file))
    #     if os.path.exists(dest_temp_file) is False:
    #         command = 'ffmpeg -i %s -b:v 360k -s 960x540 %s' % (source_file, dest_temp_file)
    #         os.system(command)
    #         shutil.move(dest_temp_file, dest_file)


    def download_mp4_m3u8(self, url, path, filename):
        print(url)
        media_name = './temp/' + str(filename) + '.mp4'
        open_path = path + str(filename) + '.mp4'
        command_1 = 'ffmpeg -i "%s" -c copy -y -bsf:a aac_adtstoasc "%s"' % (url, media_name)
        os.system(command_1)
        open_path = self.existed_file(open_path)
        shutil.move(media_name, open_path)
        return

    # 一直播单独url下载
    def download_mp4_single(self, url, filename):
        print(url, filename)
        media_name = './temp/' + str(filename) + '.mp4'
        path = 'video/temp_video/'
        self.create_date_floder(path)
        open_path = path + str(filename) + '.mp4'
        command_1 = 'ffmpeg -i "%s" -c copy -y -bsf:a aac_adtstoasc "%s"' % (url, media_name)
        os.system(command_1)
        open_path = self.existed_file(open_path)
        shutil.move(media_name, open_path)
        return

    def existed_file(self, file):
        if os.path.exists(file) is True:
            file = str(file).replace('.mp4', '_2.mp4')
            file = self.existed_file(file)
        return file
