import mysql.connector
connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root', 
    password="codewith_sumit", 
    database='python_batch_2'
)
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'
cursor = connection.cursor(dictionary=True)
user_choice = {
    1: 'INSERT',
    2: 'UPDATE',
    3: 'DELETE',
    4: 'SELECT'
}
ask_user_choice = f"""
{BLUE}Please select your choice:
Press 1 for Insert
Press 2 for Update
Press 3 for Delete
Press 4 for Select{RESET}
"""
while True:
    user_select_choice = input(ask_user_choice)
    realvalid_choice = user_choice.get(int(user_select_choice))
    if realvalid_choice:
        if realvalid_choice == 'INSERT':
            while True:
                name = input(BLUE + 'Enter name to insert: ' + RESET)
                if len(name) >= 5 and len(name) <= 20:
                    break
                else:
                    print(RED + "Please enter a valid name with Min 5 and Max 10 and all char should be Alpha" + RESET)
                    
            while True:
                email = input(BLUE + 'Enter email to insert: ' + RESET)
                if 13 <= len(email) <= 20 and email.endswith('@gmail.com'):
                    break
                else:
                    print(RED + "Invalid Email Address" + RESET)
            
            while True:
                mobile = input(BLUE + 'Enter mobile to insert: ' + RESET)
                if mobile.isdigit() and len(mobile) == 10:
                    break
                else:
                    print(RED + "Invalid Number!" + RESET)

            query = "INSERT INTO user (name, email, mobile) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, mobile))
            connection.commit()
            print(GREEN + "Record inserted successfully" + RESET)
        
        elif realvalid_choice == 'DELETE':
            while True:
                userid = input(BLUE + 'Enter the ID to delete: ' + RESET)
                if userid.isdigit():
                    break
                else:
                    print(RED + "Please enter a valid ID." + RESET)

            cursor.execute("SELECT * FROM user WHERE id = %s", (userid,))
            record = cursor.fetchone()

            if record:
                cursor.execute("DELETE FROM user WHERE id = %s", (userid,))
                connection.commit()
                print(f"Record deleted successfully.")
            else:
                print(f"No record found!!")
        else:
            print('WIP')
    else:
        print(RED + 'Invalid number!' + RESET)