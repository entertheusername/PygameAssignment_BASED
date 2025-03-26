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
        errorDict = {
            "username": None,
            "email": None,
            "password": None,
            "successful": False
        }

        try:
            usernameQuery = 'SELECT * FROM users WHERE Username = %s;'
            self.cursor.execute(usernameQuery, (username,))
            usernameData = self.cursor.fetchall()

            if not username or username == "":
                errorDict['username'] = "Invalid username!"
            elif len(username) > 15:
                errorDict['username'] = "Username too long!"
            elif usernameData:
                errorDict['username'] = "Username taken!"

            emailQuery = 'SELECT * FROM users WHERE Email = %s;'
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
        passwordHash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        emailQuery = "INSERT INTO users (Username, Email, Password, Role) VALUES (%s, %s, %s, 'Student')"
        self.cursor.execute(emailQuery, (username, email, passwordHash,))

