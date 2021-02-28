import logging

# configuring and creating the logger
logging.basicConfig(filename="C:\\AnyDocSearch\\server.log",
                    format='%(asctime)s :: %(levelname)s :: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.INFO)

class SearchUtilityLogger:
    @staticmethod
    def GetLoggerObj():
        return logging.getLogger()

