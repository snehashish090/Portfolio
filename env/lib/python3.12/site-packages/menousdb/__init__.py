# Author : Snehashish Laskar
# Date Stated : 1st November 2022
# Version : 0.1.0
# Copyright (C) Snehashish Laskar 2023
# LICENSE: MIT OPen Source Software License

# This is a python module for interacting with the
# MenousDb database. To actually use the database,
# You must download it from github link given below:
# Link :

# Import the only necessary module
import requests as req

"""
methods included:

1: readDB (key, database)
2: create-db (key, database)
3: check-db-exists (key, database)
4: del-database (key database)
5: check-table-exists (key, database, table)
6: create-table (key, database, table, attributes)
7: insert-into-table (key, database, table, values)
8: select-where (key, database, table, conditions)
9: select-columns (key, database, table, columns)
10: select-columns-where (key, database, table, columns, conditions)
11: delete-where (table, conditions)
12: delete-table (table)
13: update-table (table, conditions, values)

"""

class MenousDB:

    """
    To interact with the database, we need to create a
    and instance of the MenoudDb class. This class helps
    """

    def __init__(self, url, key, database):
        self.url = url
        self.key = key
        self.database = database
        if self.url[-1] != '/':
            self.url += '/'

    def readDb(self):

        if self.database == None:
            raise Exception('No database')

        Headers = {
            'key': self.key,
            'database': self.database
        }
        ans = req.get(self.url + 'read-db', headers=Headers)
        try:
            return ans.json()
        except:
            raise Exception(ans.text)


    def createDb(self):

        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.post(self.url + 'create-db', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def deleteDb(self):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.delete(self.url + 'del-database', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def checkDbExists(self):

        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.get(self.url + 'check-db-exists', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def createTable(self, table:str, attributes:list):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'attributes': attributes
            }

            ans = req.post(self.url + 'create-table', headers=Headers, json=Json)
            return ans.text

        except Exception as ex:
            raise ex

    def __str__(self) -> str:
        return self.database

    def checkTableExists(self, table):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            ans = req.get(self.url + 'check-table-exists', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def insertIntoTable(self, table, values):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'values': values,
            }

            ans = req.post(self.url + 'insert-into-table', headers=Headers, json=Json)
            return ans.text

        except Exception as ex:
            raise ex

    def getTable(self,table):
        if self.database is None:
            raise Exception("No database ")
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }
            ans = req.get(self.url + 'get-table', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            raise ex

    def selectWhere(self, table, conditions):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'conditions': conditions
            }

            ans = req.get(self.url + 'select-where', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def selectColumns(self, table, columns):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'columns': columns
            }

            ans = req.get(self.url + 'select-columns', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def selectColumnsWhere(self, table, columns, conditions):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'columns': columns,
                'conditions': conditions,
            }

            ans = req.get(self.url + 'select-columns-where', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def deleteWhere(self, table, conditions):
        if self.database == None:
            raise Exception('No Database')
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'conditions':conditions
            }

            ans = req.delete(self.url+"delete-where", headers = Headers, json = Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            raise ex

    def deleteTable(self, table):
            if self.database == None:
                raise Exception('No Database')
            try:
                Headers = {
                    'key': self.key,
                    'database': self.database,
                    'table': table,
                }
                ans = req.delete(self.url + "delete-table", headers=Headers)
                try:
                    return ans.json()
                except:
                    return ans.text
            except Exception as ex:
                raise ex


    def updateWhere(self, table, conditions, values):
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'conditions':conditions,
                'values':values
            }
            ans = req.post(self.url+'update-table', headers=Headers, json = Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            raise ex
        
    def getDatabases(self):
        try:
            Headers = {
                'key': self.key,
            }
            ans = req.get(self.url+'get-databases', headers=Headers)
            try:
                return ans.json()
            except:
                return ans.text()
        except Exception as ex:
            raise ex
        
        