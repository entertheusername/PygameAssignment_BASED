import pymysql
import bcrypt

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

    def register(self, username, email, password, confirmPassword):
        pass

