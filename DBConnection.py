import mysql.connector as mc

class DBConnection():
    @staticmethod
    def getConnection():
        try:
            conn = mc.connect(
                host="localhost",
                user="root",
                password="1234",
                database="hostelms"
            )
            return conn
        except Exception as e:
            print(e)