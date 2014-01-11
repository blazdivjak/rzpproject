__author__ = 'blaz'

import logging
import settings

log_filename = settings.LOG_FOLDER+settings.LOG_NAME
log_format = '%(asctime)s - %(name)s[%(process)d] - %(levelname)s - %(message)s'
logging.basicConfig(filename=log_filename,level=logging.DEBUG,format=log_format)
