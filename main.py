from image_spider import ImageSpider
import logging
logging.basicConfig(level=logging.DEBUG)


def main():
    spider = ImageSpider()
    spider.parse()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info('------------------DEBUG Image------------------')
