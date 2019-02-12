# -*- coding: utf-8 -*-
import scrapy
import requests
from factory_image import FactoryImage
from base import Session
from crawcus.settings import IMAGES_FOLDER
import sys


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['developers.google.com/android/images']
    start_urls = ['https://developers.google.com/android/images']
    session = Session()

    def parse(self, response):
        # tr_selectors = response.css("table:nth-last-child(1) tr:nth-last-child(1)") for last factory image selector 300M
        tr_selectors = response.css("tr")

        for tr in tr_selectors:
            link = tr.css("a::attr(href)").get()
            sha256 = tr.css("td:nth-last-child(1)::text").get()

            if not sha256 or not link:
                continue

            self.logger.info('------------------Factory Image------------------')
            self.logger.info('Link: %s', link)
            self.logger.info('SHA-256: %s', sha256)

            local_filename = link.split('/')[-1]
            image = self.session.query(FactoryImage).filter(FactoryImage.sha256 == sha256).first()
            if image:
                self.logger.info('This SHA-256: %s already exist with filename: %s', sha256, image.name)
                continue

            self.download_file(link, local_filename)

            self.logger.info('Saving Factory Image... %s', local_filename)
            image = FactoryImage(sha256=sha256, name=local_filename)
            self.session.add(image)
            self.session.commit()

    def download_file(self, url, local_filename):
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        path = IMAGES_FOLDER + local_filename

        self.logger.info('Downloading... %s', local_filename)
        with open(path, 'wb') as f:
            dl = 0
            total_length = int(total_length)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]\r" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        return True
