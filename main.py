import requests
from bs4 import BeautifulSoup
from image_spider import ImageSpider
import logging
logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# logger.info('Start reading database')


def main():
    spider = ImageSpider()
    spider.parse()


if __name__ == "__main__":
    main()
