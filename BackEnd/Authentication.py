import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pymysql
import bcrypt
import re
import keyring
import json
import datetime

class Authentication:
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='', host='localhost', database='capstoneproject')
        self.cursor = self.conn.cursor()

    def login(self, username, password, save):
        """
        Login function to check from the database.
        :param username: str username from user
        :param password: str password from user should correspondent of the user in database
        :param save: bool save password for silent login
        :return: str error msg or confirmation msg
        """
        try:
            query = 'SELECT * FROM students WHERE Username = %s;'
            self.cursor.execute(query, (username,))
            data = self.cursor.fetchall()
            errorMsg = {
                "banned": False,
                "loginMsg": ""
            }

            if data:
                columns = [column[0] for column in self.cursor.description]
                dbPass = data[0][columns.index('Password')]

                if data[0][columns.index('BanStatus')] != 0:
                    errorMsg["banned"] = True
                    return errorMsg

                if bcrypt.checkpw(password.encode("utf-8"), dbPass.encode("utf-8")):
                    if save:
                        file = open("../loggedInUser.json", "w")
                        data = {
                            "username": username
                        }
                        json.dump(data, file, indent=4)
                        file.close()
                        keyring.set_password("BASED", username, password)
                    errorMsg["loginMsg"] = 'Login successful!'
                    return errorMsg
                else:
                    errorMsg["loginMsg"] = 'Invalid password.'
                    return errorMsg

            else:
                errorMsg["loginMsg"] = 'User does not exist.'
                return errorMsg
        except:
            print('query failed')

    def silentLogin(self):
        """
        Logs in user without password (cookie like behaviour)
        :return: None
        """
        file = open("../loggedInUser.json", "r")
        data = json.load(file)
        file.close()
        password = keyring.get_password("BASED", data['username'])
        status = self.login(data['username'], password, False)
        if status["loginMsg"] == 'Login successful!':
            return True
        else:
            return False

    def logout(self):
        """
        Logout user from game
        :return: None
        """
        file = open("../loggedInUser.json", "r")
        data = json.load(file)
        file.close()
        keyring.delete_password("BASED", data['username'])
        file = open("../loggedInUser.json", "w")
        data = {
            "username": ""
        }
        json.dump(data, file, indent=4)
        file.close()

    def registerCheck(self, username, email, password, confirmPassword):
        """
        Confirmation check that registration is valid for system.
        :param username: str username from user
        :param email: str email from user
        :param password: str password from user
        :param confirmPassword: str confirm password from user
        :return: dict dictionary of error msgs
        """
        errorDict = {
            "username": None,
            "email": None,
            "password": None,
            "successful": False
        }

        try:
            usernameQuery = 'SELECT * FROM students WHERE Username = %s;'
            self.cursor.execute(usernameQuery, (username,))
            usernameData = self.cursor.fetchall()

            if not username or username == "":
                errorDict['username'] = "Invalid username!"
            elif len(username) > 15:
                errorDict['username'] = "Username too long!"
            elif usernameData:
                errorDict['username'] = "Username taken!"

            emailQuery = 'SELECT * FROM students WHERE Email = %s;'
            self.cursor.execute(emailQuery, (email,))
            emailData = self.cursor.fetchall()

            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if not email or email == "" or not (re.match(pattern, email)):
                errorDict['email'] = "Invalid email!"
            elif len(email) > 40:
                errorDict['email'] = "Email too long!"
            elif emailData:
                errorDict['email'] = "Email taken!"

            if not password or password == "":
                errorDict['password'] = "Invalid password!"
            elif len(password) > 30:
                errorDict['password'] = "Password too long!"
            elif password != confirmPassword:
                errorDict['password'] = "Passwords does not match!"

            if errorDict['username'] is None and errorDict['email'] is None and errorDict['password'] is None:
                errorDict['successful'] = True
                self.register(username, email, password)
                return errorDict
            else:
                return errorDict


        except:
            print('query failed')

    def register(self, username, email, password):
        """
        Registration function from system to the database.
        :param username: str username from user
        :param email: str email from user
        :param password: str password from user
        :return: None
        """
        passwordHash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        dateRegistered = datetime.date.today()

        registerQuery = "INSERT INTO students (Username, Email, Password, AdminID, DateReg) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(registerQuery, (username, email, passwordHash, 1, dateRegistered))
        self.conn.commit()

