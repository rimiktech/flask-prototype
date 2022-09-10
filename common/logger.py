import os
import sys
from datetime import datetime
import time
from config import Config

class logger:
    
    instance = None
    module = "Unknown"

    def __init__(self):
        self.__log_path = None
        self.__retryCount = 0
        if Config.ENABLE_LOGGER:
            self.__log_path = "./logs"
            if not os.path.exists(self.__log_path):
                os.makedirs(self.__log_path)
        
    def __log(self, message):
        if self.__log_path is None: return
        fileName = "{0}/{1}.{2:%m%d%y}.log"
        fileName = fileName.format(self.__log_path, os.path.basename(logger.module), datetime.now())
        try:
            with open(fileName, "a") as file:
                file.write(str(message) + "\n")
            self.__retryCount = 0
        except OSError as err:
            time.sleep(1)
            self.__retryCount = self.__retryCount + 1
            if self.__retryCount > 5:
                print(err)
                exit()
            self.__log(message)

    @staticmethod
    def log(message):
        if logger.instance is None: 
            logger.instance = logger()

        message = "{0:%Y-%m-%d %H:%M:%S} {1}".format(datetime.now(), message)
        print(message)
        logger.instance.__log(message)