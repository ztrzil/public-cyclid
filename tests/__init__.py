import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

http_handler = logging.handlers.HTTPHandler('erebus.eecs.utk.edu:9000',
    '/opt/cyclid/log', method='POST')

logger.addHandler(http_handler)
