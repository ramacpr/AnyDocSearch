import os
import PDFTokenizer as pdftokenizer

# get list of all PDF files in the path
from SearchUtility_Backend.SearchUtilityLogger import SearchUtilityLogger

input_folder_location = "D:\\Projects\\SearchUtility\\SearchUtility_Backend\\pdfFiles"
FilesList = []
fullFilePath = ""
logger = SearchUtilityLogger.GetLoggerObj()
for (root, dirs, files) in os.walk(input_folder_location):
    for filename in files:
        fullFilePath = root + "\\" + filename
        FilesList.append(fullFilePath)
if len(FilesList) <= 0:
    logger.info("No files to maintain at backend!")
else:
    tokenizerObj = pdftokenizer.PDFTokenizer()
    tokenizerObj.tokenize(FilesList)
    logger.info("Backend DB Maintenance complete.")