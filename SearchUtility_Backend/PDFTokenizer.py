import time
import MyExtendedStopWords as StopWordsHelper
import MyDatabaseManager as dbManager
import PyPDFEx as PDFHelper
from nltk.tokenize import word_tokenize as WordHelper
from nltk.stem import PorterStemmer
from wordsegment import load
from SearchUtility_Backend.SearchUtilityLogger import SearchUtilityLogger

load()


class PDFTokenizer:
    __stopWordObj = StopWordsHelper.ExtendedStopWord()
    __StopWordsList = ""
    __dbObj = None
    __logger = SearchUtilityLogger.GetLoggerObj()

    def __init__(self):
        self.__StopWordsList = self.__stopWordObj.thestopwords()
        self.__dbObj = dbManager.SqlDBManager()

    def __update_word_addresses(self, pdf_file_obj, doc_id):
        try:
            pdf_reader = PDFHelper.PdfFileReader(pdf_file_obj)
            for pageIndex in range(0, pdf_reader.numPages):
                page_obj = pdf_reader.getPage(pageIndex)
                # tokenizing
                originalPageContent = WordHelper(page_obj.extractText().lower())
                # stemming
                stemmedContent = [PorterStemmer().stem(w) for w in originalPageContent]

                # store the word db
                positionInPage = 0
                for term in stemmedContent:
                    if term not in self.__StopWordsList:
                        self.__dbObj.UpdateListing(term, doc_id, pageIndex, positionInPage)
                    positionInPage += 1
        except:
            self.__logger.fatal("Unexpected error in __update_word_addresses.")

    def tokenize(self, pdf_file_name_list):
        for pdf_file_name in pdf_file_name_list:
            self.__dbObj.SetServerUpdateState(True)
            doc_id = self.__dbObj.GetDocumentID(pdf_file_name)
            if doc_id is -1:
                continue
            start = time.clock()
            try:
                self.__logger.info("Updating database for file [" + str(doc_id) + "] " + pdf_file_name)
                pdf_file_obj = open(pdf_file_name, "rb")
                self.__update_word_addresses(pdf_file_obj, doc_id)
                self.__logger.info("Completed in " + str(time.clock() - start) + " seconds.")
            except:
                self.__logger.fatal("Unexpected error. " + pdf_file_name + " incorrectly tokenized.")
            finally:
                self.__dbObj.SetServerUpdateState(False)
                pdf_file_obj.close()
