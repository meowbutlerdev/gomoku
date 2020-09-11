# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import os
import requests
import gzip
import io
import time
import xml.etree.ElementTree as elemTree

class Index:
    def __init__(self, url='http://renjuoffline.com/games.xml.gz', data_directory='data'):
        self.url = url
        self.results = []
        self.data_directory = data_directory

    # 기보 저장
    def download_files(self):
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)

        response = requests.get(self.url, stream=True)
        file = io.BytesIO(response.content)

        with gzip.GzipFile(fileobj=file) as f:
            reader = elemTree.parse(f)
            games = reader.iter(tag='game')
            for game in games:
                code = game.find('id')
                creation_time = game.find('creation_time')
                board = game.find('board')
                if board.text is not None:
                    tm = time.gmtime(int(creation_time.text))
                    name = f'{self.data_directory}/{tm.tm_year}{str(tm.tm_mon).zfill(2)}{str(tm.tm_mday).zfill(2)}-{code.text}.xml'
                    if not os.path.isfile(name):
                        elemTree.ElementTree(game).write(name)