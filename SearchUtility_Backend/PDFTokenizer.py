import time
import MyExtendedStopWords as StopWordsHelper
import MyDatabaseManager as dbManager
import PyPDF2 as PDFHelper
from nltk.tokenize import word_tokenize as WordHelper
from nltk.stem import PorterStemmer
from wordsegment import load
load()


class PDFTokenizer:
    __stopWordObj = StopWordsHelper.ExtendedStopWord()
    # __StemmingHelper = PorterStemmer()
    __StopWordsList = ""
    __dbObj = None

    def __init__(self):
        self.__StopWordsList = self.__stopWordObj.thestopwords()
        self.__dbObj = dbManager.SqlDBManager()

    def __update_word_addresses(self, pdf_file_path, doc_id):
        try:
            pdf_file_obj = open(pdf_file_path, "rb")
            pdf_reader = PDFHelper.PdfFileReader(pdf_file_obj)
            for pageIndex in range(0, pdf_reader.numPages):
                page_obj = pdf_reader.getPage(pageIndex)

                # tokenizing
                originalPageContent = WordHelper(page_obj.extractText().lower())

                # stemming
                stemmedContent = [PorterStemmer().stem(w) for w in originalPageContent]

                # stop word removal
                pageWords = [w for w in stemmedContent if w not in self.__StopWordsList]

                # store the word occurrences in the db
                for term in pageWords:
                    [self.__dbObj.AddToWordTable(term, doc_id, pageIndex, str(i))
                     for i, n in enumerate(stemmedContent) if n == term]
        finally:
            pdf_file_obj.close()
        return 1


    def tokenize(self, pdf_file_name_list):
        for pdf_file_name in pdf_file_name_list:
            doc_id = self.__dbObj.GetDocumentID(pdf_file_name)
            print("document: ", pdf_file_name, " ID retrieved:", str(doc_id))
            if doc_id is -1:
                continue
            start = time.clock()
            print('Updating db.....')
            self.__update_word_addresses(pdf_file_name, doc_id)
            print("DONE! Time Taken = ", str(time.clock() - start))
