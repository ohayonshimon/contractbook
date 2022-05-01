import requests

from log import logger
import config


def get():
    url = config.URL
    try:
        logger.info('Getting dataset from source')
        dataset = requests.get(url).json()

    except Exception as exception:
        logger.exception('Failed to get dataset from source, Error: %s',
                         exception)
    return dataset
