import mysql.connector as sql

from SearchUtility_Backend.SearchUtilityLogger import SearchUtilityLogger


class MySQLCommands:
    @staticmethod
    def CreateDataBase():
        return "CREATE DATABASE IF NOT EXISTS SearchUtility"

    @staticmethod
    def UseDataBase():
        return "USE SearchUtility"

    @staticmethod
    def CreateServerStateTable():
        return "CREATE TABLE IF NOT EXISTS state(dummy INT)"

    @staticmethod
    def DropServerStateTable():
        return "DROP TABLE state"

    @staticmethod
    def CreateOccurancesTable():
        return "CREATE TABLE IF NOT EXISTS occurances(ID INT PRIMARY KEY AUTO_INCREMENT,wordID INT,docID INT,pageNum INT," \
               "positionInPage INT,FOREIGN KEY(docID) REFERENCES documents(dID),FOREIGN KEY(wordID) REFERENCES " \
               "vocabulary(wID)) "

    @staticmethod
    def CreateVocabularyTable():
        return "CREATE TABLE IF NOT EXISTS vocabulary(wID INT PRIMARY KEY AUTO_INCREMENT,word VARCHAR(255))"

    @staticmethod
    def CreateDocTable():
        return "CREATE TABLE IF NOT EXISTS documents(dID INT PRIMARY KEY AUTO_INCREMENT,file VARCHAR(500))"

    @staticmethod
    def InsertDocument():
        return "INSERT INTO documents(file) VALUES (%s)"

    @staticmethod
    def InsertWord():
        return "INSERT INTO vocabulary(word) VALUES (%s)"

    @staticmethod
    def InsertOccurance():
        return "INSERT INTO occurances(wordID, docID, pageNum, positionInPage) VALUES (%s, %s, %s, %s)"

    @staticmethod
    def GetDocumentID():
        return "SELECT dID FROM documents WHERE file = %s"

    @staticmethod
    def GetWordID():
        return "SELECT wID FROM vocabulary WHERE word = %s"




class SqlDBManager:
    __db = None
    __dbCursor = None
    __logger = SearchUtilityLogger.GetLoggerObj()

    def __init__(self):
        self.__db = sql.connect(
            host="localhost",
            user="root",
            password="Priya12#"
        )
        if not self.__db is None:
            self.__logger.info("DB Connection Status: Pass")
            self.__dbCursor = self.__db.cursor(buffered=True)
            self.__initializeDataSource()
        else:
            self.__logger.info("DB Connection Status: Fail")

    def __initializeDataSource(self):
        self.__ExecuteQuery(MySQLCommands.CreateDataBase())
        self.__ExecuteQuery(MySQLCommands.UseDataBase())
        self.__ExecuteQuery(MySQLCommands.CreateDocTable())
        self.__ExecuteQuery(MySQLCommands.CreateVocabularyTable())
        self.__ExecuteQuery(MySQLCommands.CreateOccurancesTable())
        self.__logger.info("SearchUtility db initialized")

    def __insertToDocTable(self, fullFilePath):
        [docExists, docID] = self.__isDocExists(fullFilePath)
        if not docExists:
            self.__ExecuteQuery(MySQLCommands.InsertDocument(), (fullFilePath,))
            docIDs = self.__ExecuteQuery(MySQLCommands.GetDocumentID(), (fullFilePath,))
            docID = docIDs[0][0]
        return docID

    def __isDocExists(self, fullFilePath):
        return self.__isExists(MySQLCommands.GetDocumentID(), fullFilePath)

    def __insertToWordTable(self, word):
        [wordExists, wordID] = self.__isWordExists(word)
        if not wordExists:
            self.__ExecuteQuery(MySQLCommands.InsertWord(), (word,))
            wordIDs = self.__ExecuteQuery(MySQLCommands.GetWordID(), (word,))
            wordID = wordIDs[0][0]
        return wordID

    def __isWordExists(self, word):
        return self.__isExists(MySQLCommands.GetWordID(), word)

    def __isExists(self, cmd, ID):
        IDs = self.__ExecuteQuery(cmd, (ID,))
        if len(IDs) is 0 or IDs is None:
            return [False, -1]
        return [True, IDs[0][0]]

    def __insertToOccuranceTable(self, wordID, docID, pageNum, positionInPage):
        self.__ExecuteQuery(MySQLCommands.InsertOccurance(), (wordID, docID, pageNum, positionInPage))

    # The method will update document table and
    # return new docID if new file name is passed
    # or return the existing docID


    def __fetchDocID(self, pdfFullFilePath):
        return self.__insertToDocTable(pdfFullFilePath)

    def __fetchWordID(self, word):
        return self.__insertToWordTable(word)

    def __ExecuteQuery(self, opr, params=None, debugMode=False):
        response = None
        for res in self.__dbCursor.execute(opr, params, multi=True):
            if res.with_rows:
                response = res.fetchall()
                if debugMode:
                    self.__logger.debug("Rows produced by statement '{}':".format(res.statement))
                    self.__logger.debug(response)
            else:
                response = None
                if debugMode:
                    self.__logger.debug("Number of rows affected by statement '{}': {}".format(res.statement, res.rowcount))
        self.__db.commit()
        return response

    def UpdateListing(self, word, docID, pageNumber, positionInPage):
        # Check if this word is in the vocabulary table and get its wordID
        wordID = self.__fetchWordID(word)
        return self.__insertToOccuranceTable(wordID, docID, pageNumber, positionInPage)

    def GetDocumentID(self, pdfFullFilePath):
        return self.__fetchDocID(pdfFullFilePath)

    def SetServerUpdateState(self, isUpdating):
        if isUpdating:
            self.__ExecuteQuery(MySQLCommands.CreateServerStateTable())
        else:
            self.__ExecuteQuery(MySQLCommands.DropServerStateTable())


