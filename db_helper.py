import mysql.connector as connector
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


class DBHelper:
    def __init__(self):
        self.con =connector.connect(host="localhost",user ="architaggarwal24",password="Aarchit@2401",database="pythontest")
        query = 'create table if not exists user(userId int primary key,userName varchar(200), phone varchar(12))'
        cur = self.con.cursor()
        cur.execute(query)
        logging.info("User table creation checked/created successfully.")
    
    
    
    def insert_user(self,userid, username,phone):
        try:
            query="insert into user (userId,userName,phone) values({},'{}','{}')".format(userid,username,phone)
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()
            logging.info("User inserted successfully")

        except connector.Error as err:
            print(f"Database Error: {err}")
    
    
    
    def fetch_all(self):
        try:
            query ="select * from user"
            cur = self.con.cursor()
            cur.execute(query)
            for row in cur:
                print("userId : ",row[0])
                print("user name : ",row[1])
                print("user phone : ",row[2])
                print()
                print()
            logging.info("User fetched successfully")

        except connector.Error as err:
            print(f"Database Error: {err}")
    
    

    def delete_user(self,userId):
        try:
            query = "delete from user where userId={}".format(userId)
            c= self.con.cursor()
            c.execute(query)
            self.con.commit()
            logging.info("User deleted successfully")

        except connector.Error as err:
            print(f"Database Error: {err}")
    


    def update_user(self,userId,newName,newPhone):
        try:
            query ="update user set userName='{}', phone='{}' where userId={}".format(newName,newPhone,userId)
            cur =self.con.cursor()
            cur.execute(query)
            self.con.commit()
            logging.info("User updated successfully")
        except connector.Error as err:
            print(f"Database Error: {err}")