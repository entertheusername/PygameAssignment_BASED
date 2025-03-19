import pymysql
import bcrypt
import re

class Authentication:
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='', host='localhost', database='capstoneproject')
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        try:
            query = 'SELECT * FROM users WHERE Username = %s;'
            self.cursor.execute(query, (username,))
            data = self.cursor.fetchall()
            if data:
                columns = [column[0] for column in self.cursor.description]
                dbPass = data[0][columns.index('Password')]
                password = password.strip()

                if bcrypt.checkpw(password.encode("utf-8"), dbPass.encode("utf-8")):
                    return 'Login successful!'
                else:
                    return 'Invalid password.'

            else:
                return 'User does not exist.'

        except:
            print('query failed')

    def registerCheck(self, username, email, password, confirmPassword):
        errorList = []

        try:
            usernameQuery = 'SELECT * FROM users WHERE Username = %s;'
            self.cursor.execute(usernameQuery, (username,))
            usernameData = self.cursor.fetchall()

            if not username or username == "":
                errorList.append("Invalid username!")
            elif usernameData:
                errorList.append("Username taken!")

            emailQuery = 'SELECT * FROM users WHERE Email = %s;'
            self.cursor.execute(emailQuery, (email,))
            emailData = self.cursor.fetchall()

            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if not email or email == "" or not (re.match(pattern, email)):
                errorList.append("Invalid email!")
            elif emailData:
                errorList.append("Email taken!")

            if not password or password == "":
                errorList.append("Invalid password!")
            elif password != confirmPassword:
                errorList.append("Passwords does not match!")

            if len(errorList) == 0:
                errorList.append("Register successful!")
                self.register(username, email, password)
                return errorList
            else:
                return errorList


        except:
            print('query failed')

    def register(self, username, email, password):
        passwordHash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        emailQuery = "INSERT INTO users (Username, Email, Password, Role) VALUES (%s, %s, %s, 'Student')"
        self.cursor.execute(emailQuery, (username, email, passwordHash,))

