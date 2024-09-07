from myproject import DBHelper
def main():
    db =DBHelper()
    # db.fetch_all()
    while True:
        print("************WELCOME*********")
        print()
        
        print("PRESS 1 to insert new user")
        print("PRESS 2 to display all user")
        print("PRESS 3 to delete user")
        print("PRESS 4 to update user")
        print("PRESS 5 to exit program")
        print()
        try:
            choice= int(input())
            if choice==1:
                uid = int(input("Enter user id:"))
                username=input("enter user name")
                userphone =input("enter user phone:")
                db.insert_user(uid,username,userphone)
                pass
            elif choice==2:
                db.fetch_all()
                pass
            elif choice==3:
                uid = int(input("Enter user id:"))
                db.delete_user(uid)
                pass
            elif choice==4:
                uid = int(input("Enter user id:"))
                username=input("new name")
                userphone =input("new phone:")
                db.update_user(uid,username,userphone)
                pass
            elif choice==5:
                break
            else:
                print("Invalid input ! try again")
        except Exception as e:
            print(e)
            print("Invalid details ! Try again")

if __name__ == "__main__":
    main()
       
        