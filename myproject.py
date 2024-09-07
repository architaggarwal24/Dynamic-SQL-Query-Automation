import mysql.connector as connector
class DBHelper:
    def __init__(self):
        self.con =connector.connect(host="localhost",user ="sakarwl123",password="Saksham@1010",database="pythontest")
        query = 'create table if not exists user(userId int primary key,userName varchar(200), phone varchar(12))'
        cur = self.con.cursor()
        cur.execute(query)
        print("Created")
    # insert
    def insert_user(self,userid, username,phone):
        query="insert into user(userId,userName,phone) values({},'{}','{}')".format(userid,username,phone)
        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("user saved to db")
    # fetch all
    def fetch_all(self):
        query ="select * from user"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            print("userId : ",row[0])
            print("user name : ",row[1])
            print("user phone : ",row[2])
            print()
            print()
    def delete_user(self,userId):
        query = "delete from user where userId={}".format(userId)
        print(query)
        c= self.con.cursor()
        c.execute(query)
        self.con.commit()
        print("deletd")
    # update
    def update_user(self,userId,newName,newPhone):
        query ="update user set userName='{}',phone='{}'where userId={}".format(newName,newPhone,userId)
        print(query)
        cur =self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("updated")
