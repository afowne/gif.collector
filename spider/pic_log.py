import logging

logging.basicConfig(filename='log\ERROR.log', level=logging.INFO, format='%(asctime)s.%(msecs)d---%(message)s', datefmt='%Y/%m/%d %I:%M:%S')

def log_print(content):
    logging.info(content)
    print(content)
