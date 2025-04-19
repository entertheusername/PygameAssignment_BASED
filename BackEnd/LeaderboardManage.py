import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pymysql
import re
import json


class LeaderboardManage:
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='', host='localhost', database='capstoneproject')
        self.cursor = self.conn.cursor()
        self.high_score = {}

    def scoreSubmission(self, score, gameMode, timeTaken):
        """
        Submit score after game is finish.
        :param score: score when game ended
        :param gameMode: which game mode chosen
        :param timeTaken: time taken from start to end game
        :return: None
        """
        file = open("../loggedInUser.json", "r")
        data = json.load(file)
        username = data['username']

        retrieveIDQuery = 'SELECT * FROM students WHERE Username = %s;'
        self.cursor.execute(retrieveIDQuery, (username,))
        data = self.cursor.fetchall()
        if data:
            columns = [column[0] for column in self.cursor.description]
            StudentID = data[0][columns.index('StudentID')]
        else:
            print(
                "If this comes out this is the most insane bug i've ever seen cuz this "
                "does not happen cuz the username from the cache is gone and that is not "
                "possible according to the software"
            )
            return

        date = datetime.date.today()

        submissionQuery = ("INSERT INTO scores (StudentID, Score, GameMode, TimeTaken, DateSubmitted) "
                           "VALUES (%s, %s, %s, %s, %s)")
        self.cursor.execute(submissionQuery, (StudentID, score, gameMode, timeTaken, date,))
        self.conn.commit()
        # Get high score if this is a new record
        current_high = self.get_high_score(gameMode)
        if score > current_high:
            self.high_score = score
        else:
            self.high_score = current_high

    def get_high_score(self, game_mode):
        query = ("SELECT MAX(Score) FROM scores "
                 "WHERE GameMode = %s")
        self.cursor.execute(query, (game_mode,))
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def retrieveLeaderboard(self, gameMode, page, monthly=False):
        file = open("../loggedInUser.json", "r")
        data = json.load(file)
        username = data['username']
        extraQuery = ""

        offset = (page - 1) * 5

        if monthly:
            extraQuery = ("AND YEAR(DateSubmitted) = YEAR(CURDATE())"
                          "AND MONTH(DateSubmitted) = MONTH(CURDATE())")

        retrieveOtherQuery = ("SELECT "
                              "ROW_NUMBER() OVER (ORDER BY s.Score DESC) AS Placement, "
                              "st.Username, s.TimeTaken, s.Score "
                              "FROM scores s "
                              "JOIN students st ON s.StudentID = st.StudentID "
                              "WHERE s.ScoreID = ( "
                              "SELECT ScoreID "
                              "FROM scores "
                              f"WHERE StudentID = s.StudentID AND GameMode = '{gameMode}'"
                              f"{extraQuery}"
                              "ORDER BY Score DESC "
                              "LIMIT 1 "
                              ") "
                              f"LIMIT 6 OFFSET {offset}; ")

        self.cursor.execute(retrieveOtherQuery)
        leaderboardData = self.cursor.fetchall()
        leaderboard = []
        inBoard = False

        for i in leaderboardData:
            leaderboardRow = list(i)
            leaderboardRow[0] = str(leaderboardRow[0])
            leaderboardRow[-1] = str(leaderboardRow[-1])
            if leaderboardRow[1] == username:
                inBoard = True
            else:
                pass
            leaderboard.append(leaderboardRow)

        if not inBoard and len(leaderboard) > 5:
            studentQuery = ("SELECT Placement, Username, TimeTaken, Score "
                            "FROM ( "
                            "SELECT "
                            "ROW_NUMBER() OVER (ORDER BY s.Score DESC) AS Placement, "
                            "st.Username, s.TimeTaken, s.Score "
                            "FROM scores s "
                            "JOIN students st ON s.StudentID = st.StudentID "
                            "WHERE s.ScoreID = ( "
                            "SELECT ScoreID "
                            "FROM scores "
                            f"WHERE StudentID = s.StudentID AND GameMode = '{gameMode}'"
                            f"{extraQuery}"
                            "ORDER BY Score DESC "
                            "LIMIT 1 "
                            ") "
                            ") AS PlacementScores "
                            f"WHERE Username = '{username}';")
            self.cursor.execute(studentQuery)
            studentData = self.cursor.fetchall()
            # print(studentData)

            if studentData:
                leaderboard.pop(-1)
                studentRow = list(studentData[0])
                studentRow[0] = str(studentRow[0])
                studentRow[-1] = str(studentRow[-1])
                if int(studentRow[0]) < int(leaderboard[0][0]):
                    leaderboard.insert(0, studentRow)
                else:
                    leaderboard.append(studentRow)
        return leaderboard


# if __name__ == "__main__":
#     main = LeaderboardManage()
#     # main.scoreSubmission(1500, "conversion", "12:60:90")
#     main.retrieveLeaderboard("conversion", True)
