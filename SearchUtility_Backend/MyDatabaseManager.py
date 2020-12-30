import mysql.connector as sql


def CreateDataBase():
    return "CREATE DATABASE IF NOT EXISTS SearchUtility"


def UseDataBase():
    return "USE SearchUtility"


def CreateWordsTable():
    return "CREATE TABLE IF NOT EXISTS vocabulary(ID INT PRIMARY KEY AUTO_INCREMENT,word VARCHAR(255),docID INT,pageNum INT,lineNum INT,FOREIGN KEY(docID) REFERENCES documents(ID))"


def CreateDocTable():
    return "CREATE TABLE IF NOT EXISTS documents(ID INT PRIMARY KEY AUTO_INCREMENT,file VARCHAR(500))"


def InsertDocument():
    return "INSERT INTO documents(file) VALUES (%s)"


def GetDocumentID():
    return "SELECT ID FROM documents WHERE file = %s"


def InsertWord():
    return "INSERT INTO vocabulary(word, docID, pageNum, lineNum) VALUES (%s, %s, %s, %s)"


class SqlDBManager:
    __db = None
    __dbCursor = None
    def __init__(self):
        self.__db = sql.connect(
            host="localhost",
            user="root",
            password="Priya12#"
        )
        if not self.__db is None:
            print("DB Connection Status: Pass")
            self.__dbCursor = self.__db.cursor(buffered=True)
            self.__initializeDataSource()
        else:
            print("DB Connection Status: Fail")

    def __initializeDataSource(self):
        self.__ExecuteQuery(CreateDataBase())
        self.__ExecuteQuery(UseDataBase())
        self.__ExecuteQuery(CreateDocTable())
        self.__ExecuteQuery(CreateWordsTable())
        print("SearchUtility db initialized")

    def __insertToDocTable(self, fullFilePath):
        [docExists, docID] = self.__isDocExists(fullFilePath)
        if not docExists:
            self.__ExecuteQuery(InsertDocument(), (fullFilePath,))
            docIDs = self.__ExecuteQuery(GetDocumentID(), (fullFilePath,))
            docID = docIDs[0][0]
        return docID

    def __isDocExists(self, fullFilePath):
        docIDs = self.__ExecuteQuery(GetDocumentID(), (fullFilePath,))
        if len(docIDs) is 0 or docIDs is None:
            return [False, -1]
        return [True, docIDs[0][0]]

    def __insertToWordTable(self, word, docID, pageNum, lineNum):
        self.__ExecuteQuery(InsertWord(), (word, docID, pageNum, lineNum))

    # The method will update document table and
    # return new docID if new file name is passed
    # or return the existing docID
    def GetDocumentID(self, pdfFullFilePath):
        return self.__insertToDocTable(pdfFullFilePath)

    def AddToWordTable(self, word, docID, pageNumber, lineNumber):
        return self.__insertToWordTable(word, docID, pageNumber, lineNumber)

    def __ExecuteQuery(self, opr, params=None, debugMode=False):
        response = None
        for res in self.__dbCursor.execute(opr, params, multi=True):
            if res.with_rows:
                response = res.fetchall()
                if debugMode:
                    print("Rows produced by statement '{}':".format(res.statement))
                    print(response)
            else:
                response = None
                if debugMode:
                    print("Number of rows affected by statement '{}': {}".format(res.statement, res.rowcount))
        self.__db.commit()
        return response
