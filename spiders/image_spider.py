import requests
import sys
from bs4 import BeautifulSoup
from spiders.spider import Spider
from models.factory_image import FactoryImage


class ImageSpider(Spider):
    name = 'images'

    def parse(self):
        print("Da")
        page = requests.get("https://developers.google.com/android/images")
        soup = BeautifulSoup(page.content, 'html.parser')
        tr_selectors = soup.find_all("tr")

        for tr in tr_selectors:
            link = tr.a['href']
            sha256 = tr('td')[-1].get_text()

            if not sha256 or not link:
                continue

            self.logger.info('------------------Factory Image------------------')
            self.logger.debug('------------------DEBUG Image------------------')
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

        path = 'images/' + local_filename

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
