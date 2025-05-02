# Import modules
import sys
import os

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pymysql
import json

class TutorialManage:
    """
    Manage tutorial-related functionalities and update the tutorial status in the database.
    """
    def __init__(self):
        """
        Initialise the TutorialManage class and connect to database.
        """
        self.conn = pymysql.connect(user='root', password='', host='localhost', database='capstoneproject')
        # self.conn = pymysql.connect(user='root', password='vKCdduMYpg', host='34.124.212.17', database='capstone',
        #                             port=3306) # Need to add the person's ip lmao idk anymore
        self.cursor = self.conn.cursor()

    def checkTutorial(self):
        """
        Check if the user has done the tutorial or not.
        :return: A boolean, true if the user has completed the tutorial, false otherwise.
        """
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
        """
        Change tutorial from to finish as user finish tutorial.
        :return: None
        """
        file = open("../loggedInUser.json", "r")
        jsonData = json.load(file)
        file.close()

        tutorialQuery = f"UPDATE students SET TutorialStat = %s WHERE Username = '{jsonData['username']}'"
        self.cursor.execute(tutorialQuery, (1,))
        self.conn.commit()
