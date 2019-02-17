from image_spider import ImageSpider
import logging
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    try:
        spider = ImageSpider()
        spider.parse()
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info('------------------Closing spider (shutdown)------------------')
