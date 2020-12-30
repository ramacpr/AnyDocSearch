import os
import PDFTokenizer as pdftokenizer

# get list of all PDF files in the path
input_folder_location = "D:\\Projects\\SearchUtility\\SearchUtility_Backend\\pdfFiles"
FilesList = []
fullFilePath = ""
for (root, dirs, files) in os.walk(input_folder_location):
    for filename in files:
        fullFilePath = root + "\\" + filename
        FilesList.append(fullFilePath)
if len(FilesList) <= 0:
    print("No files to maintain at backend!")
else:
    tokenizerObj = pdftokenizer.PDFTokenizer()
    tokenizerObj.tokenize(FilesList)
    print("Backend DB Maintenance complete.")