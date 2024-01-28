import logging

log_format = logging.Formatter('%(asctime)s %(lineno)d %(levelname)8s:%(message)s')

logging.basicConfig(format='%(asctime)s %(lineno)d %(levelname)8s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)

# log를 파일에 출력
file_handler = logging.FileHandler(directory)  #log파일 저장 경로
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)


logger.info("info ment")
logger.debug("debug ment")
logger.warning("warning ment")
logger.error("error ment")