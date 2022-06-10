import os
import mysql.connector

class DatabaseAssistant:
    def __init__(self):
        self.__initRead()
        self.__initWrite()

    def __initRead(self):
        self.db_read = mysql.connector.connect(
            host= os.environ["dbHostPod"],
            user= os.environ["dbUserPod"],
            password= os.environ["dbPasswdPod"],
            database= os.environ["dbNamePod"],
            connect_timeout=28800
        )
        self.readCursor = self.db_read.cursor()

    def __initWrite(self):
        self.db_write = mysql.connector.connect(
            host= os.environ["dbHostMaster"],
            user= os.environ["dbUserMaster"],
            password= os.environ["dbPasswdMaster"],
            database= os.environ["dbNameMaster"],
            connect_timeout=28800
        )
        self.writeCursor = self.db_write.cursor()


    def ReadQuery(self, query, vals=[]):
        try:
            self.readCursor.execute(query, vals)
        except Exception as e:
            self.__initRead()
            self.readCursor.execute(query, vals)
        
        return self.readCursor.fetchall()

    def WriteQuery(self, query, vals=[]):
        try:
            self.writeCursor.execute(query, vals)
            self.db_write.commit()
        except Exception as e:
            self.__initWrite()
            self.writeCursor.execute(query, vals)
            self.db_write.commit()