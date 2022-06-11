import os
import mysql.connector

class DatabaseAssistant:
    def __initRead(self):
        self.db_read = mysql.connector.connect(
            host= os.environ["dbHostPod"],
            user= os.environ["dbUserPod"],
            password= os.environ["dbPasswdPod"],
            database= os.environ["dbNamePod"]
        )
        self.readCursor = self.db_read.cursor(buffered=True)

    def __initWrite(self):
        self.db_write = mysql.connector.connect(
            host= os.environ["dbHostMaster"],
            user= os.environ["dbUserMaster"],
            password= os.environ["dbPasswdMaster"],
            database= os.environ["dbNameMaster"]
        )
        self.writeCursor = self.db_write.cursor(buffered=True)


    def ReadQuery(self, query, vals=[]):
        self.__initRead()
        self.readCursor.execute(query, vals)
            
        return self.readCursor.fetchall()

    def ReadQueryMaster(self, query, vals=[]):
        return self.WriteQuery(query, vals, True)

    def WriteQuery(self, query, vals=[], read=False):
        self.__initWrite()
        self.writeCursor.execute(query, vals)
           
        if not read:
            self.db_write.commit()
        else:
            return self.writeCursor.fetchall()