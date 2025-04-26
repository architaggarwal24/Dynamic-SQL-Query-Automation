from db_helper import DBHelper


def main():
    db =DBHelper()
    while True:
        print("\n****** Welcome to the User Management System ******\n")
        print("Press 1: Insert new user")
        print("Press 2: Display all users")
        print("Press 3: Delete user")
        print("Press 4: Update user")
        print("Press 5: Exit program\n")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        
        if choice==1:
            userid = input("Enter user id: ")
            if not userid.isdigit():
                print("User ID must be a number.")
                continue
            userid = int(userid)
            username=input("Enter username: ")
            userphone =input("Enter user phone: ")
            db.insert_user(userid,username,userphone)
        
        
        elif choice==2:
            db.fetch_all()
        
        
        elif choice==3:
            userid = input("Enter user id: ")
            if not userid.isdigit():
                print("User ID must be a number.")
                continue
            userid = int(userid)
            db.delete_user(userid)
        
        
        elif choice==4:
            userid = input("Enter user id: ")
            if not userid.isdigit():
                print("User ID must be a number.")
                continue
            userid = int(userid)
            username=input("Enter new name: ")
            userphone =input("Enter new phone: ")
            db.update_user(userid,username,userphone)
       
        
        elif choice==5:
            print("Thank you for using the system. Goodbye!")
        
        
        else:
            print("Invalid input! Try again")



if __name__ == "__main__":
    main()
       
        