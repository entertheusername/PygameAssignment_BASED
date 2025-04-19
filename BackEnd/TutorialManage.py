import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pymysql
import json

class TutorialManage:
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='', host='localhost', database='capstoneproject')
        self.cursor = self.conn.cursor()

    def checkTutorial(self):
        file = open("../loggedInUser.json", "r")
        jsonData = json.load(file)
        file.close()
        try:
            query = 'SELECT * FROM students WHERE Username = %s;'
            self.cursor.execute(query, (jsonData['username'],))
            userData = self.cursor.fetchall()

            if userData:
                columns = [column[0] for column in self.cursor.description]
                status = userData[0][columns.index('TutorialStat')]
                return True if status == 1 else False
            else:
                print("This shud not exist also so skibidi.")
                return False
        except:
            print("This shud not exist so skibidi.")
            return None

    def updateTutorial(self):
        file = open("../loggedInUser.json", "r")
        jsonData = json.load(file)
        file.close()

        tutorialQuery = f"UPDATE students SET TutorialStat = %s WHERE Username = '{jsonData['username']}'"
        self.cursor.execute(tutorialQuery, (1,))
        self.conn.commit()