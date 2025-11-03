import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

db_cursor = db_connection.cursor(dictionary=True)

MENU_CHOICES = {
    '1': 'INSERT',
    '2': 'UPDATE',
    '3': 'DELETE',
    '4': 'SELECT'
}

MAIN_MENU_PROMPT = f"""
{BLUE}
Please select an operation:
1. Insert a new record
2. Update an existing record
3. Delete a record
4. Select/View records
{RESET}
"""

def get_valid_input(prompt, validation_type, current_value=None):
    while True:
        user_input = input(prompt).strip()
        
        if validation_type in ['name', 'email', 'mobile'] and not user_input and current_value is not None:
            return current_value

        is_valid = False
        error_message = ""
        
        if validation_type == 'name':
            if 5 <= len(user_input) <= 20:
                is_valid = True
            else:
                error_message = "Name must be between 5 and 20 characters."
                
        elif validation_type == 'email':
            if user_input.endswith("@gmail.com") and 13 <= len(user_input) <= 20:
                is_valid = True
            else:
                error_message = "Email must end with @gmail.com and be 13-20 characters long."
                
        elif validation_type == 'mobile':
            if len(user_input) == 10 and user_input.isnumeric():
                is_valid = True
            else:
                error_message = "Mobile number must be exactly 10 digits and numeric."
                
        elif validation_type == 'id':
            if user_input.isnumeric() and int(user_input) > 0:
                is_valid = True
            else:
                error_message = "ID must be a positive number."

        if is_valid:
            return user_input
        else:
            print(f"{RED}Invalid input: {error_message}{RESET}")

def display_record(record):
    
    print(f"ID:     {record.get('id', 'N/A')}")
    print(f"Name:   {record.get('name', 'N/A')}")
    print(f"Email:  {record.get('email', 'N/A')}")
    print(f"Mobile: {record.get('mobile', 'N/A')}")

def handle_insert():
    new_name = get_valid_input('Enter name to insert (5-20 chars): ', 'name')
    new_email = get_valid_input('Enter email to insert (@gmail.com, 13-20 chars): ', 'email')
    new_mobile = get_valid_input('Enter mobile to insert (10 digits): ', 'mobile')
    
    insert_query = "INSERT INTO user (name, email, mobile) VALUES (%s, %s, %s)"
    db_cursor.execute(insert_query, (new_name, new_email, new_mobile))
    db_connection.commit()
    print(f"{GREEN}Record inserted successfully!{RESET}")

def handle_select():
    db_cursor.execute("SELECT COUNT(*) AS total_count FROM user")
    total_records = db_cursor.fetchone()['total_count']
    
    if total_records == 0:
        print(f"{YELLOW}The 'user' table is currently empty.{RESET}")
        return
        
    print(f"Total records found: {total_records}")
    
    records_displayed = 0
    
    while records_displayed < total_records:
        remaining = total_records - records_displayed
        
        while True:
            row_choice = get_valid_input("How many rows do you want to see? ", 'id')
            rows_to_display = min(int(row_choice), remaining)
            break

        query = "SELECT id, name, email, mobile FROM user ORDER BY id ASC LIMIT %s OFFSET %s"
        db_cursor.execute(query, (rows_to_display, records_displayed))
        records = db_cursor.fetchall()
        
        for record in records:
            display_record(record)
            
        records_displayed += len(records)
        remaining = total_records - records_displayed
        
        if remaining > 0:
            while True:
                next_action = input(f"{BLUE}Records displayed: {records_displayed}/{total_records}. Remaining: {remaining}.\n"
                                    "1. See more\n2. Return to Main Menu\nEnter choice: {RESET}").strip()
                if next_action == '1':
                    break
                elif next_action == '2':
                    return
                else:
                    print(f"{RED}Invalid choice. Enter 1 or 2.{RESET}")
        else:
             while True:
                next_action = input(f"{BLUE}All data displayed. 2. Return to Main Menu\nEnter choice: {RESET}").strip()
                if next_action == '2':
                    return
                else:
                    print(f"{RED}Invalid choice. Enter 2.{RESET}")

def handle_delete():
    db_cursor.execute("SELECT id, name FROM user ORDER BY id ASC")
    all_users = db_cursor.fetchall()
    if not all_users:
        print(f"{YELLOW}No records to delete.{RESET}")
        return

    print("Existing IDs for reference:")
    for user in all_users:
        print(f"ID: {user['id']} - Name: {user['name']}")
        
    while True:
        delete_id_input = get_valid_input("Enter ID of the record to delete: ", 'id')
        delete_id = int(delete_id_input)
        
        check_query = "SELECT id FROM user WHERE id = %s"
        db_cursor.execute(check_query, (delete_id,))
        record_exists = db_cursor.fetchone()
        
        if record_exists:
            break
        print(f"{RED}ID {delete_id} not found in the table.{RESET}")

    delete_query = "DELETE FROM user WHERE id = %s"
    db_cursor.execute(delete_query, (delete_id,))
    
    if db_cursor.rowcount > 0:
        db_connection.commit()
        print(f"{GREEN}Record ID {delete_id} deleted successfully!{RESET}")
    else:
        print(f"{YELLOW}Record ID {delete_id} was not deleted.{RESET}")
            
def handle_update():
    db_cursor.execute("SELECT id, name, email, mobile FROM user ORDER BY id ASC")
    all_records = db_cursor.fetchall()
    
    if not all_records:
        print(f"{YELLOW}Nothing to update. Table is empty.{RESET}")
        return

    print("Current Records:")
    for record in all_records:
        display_record(record)
        
    record_to_update = None
    update_id = None
    while True:
        update_id_input = get_valid_input("Enter the ID of the record you wish to update: ", 'id')
        update_id = int(update_id_input)
        
        check_query = "SELECT id, name, email, mobile FROM user WHERE id = %s"
        db_cursor.execute(check_query, (update_id,))
        record_to_update = db_cursor.fetchone()

        if record_to_update:
            break
        print(f"{RED}ID {update_id} not found in the table.{RESET}")
            
    print(f"\n{YELLOW}Current Data for ID {update_id}:{RESET}")
    display_record(record_to_update)
    print(f"{BLUE}Enter new values. Leave blank to keep the current value.{RESET}")

    new_name = get_valid_input(f"New Name (Current: {record_to_update['name']}): ", 'name', record_to_update['name'])
    new_email = get_valid_input(f"New Email (Current: {record_to_update['email']}): ", 'email', record_to_update['email'])
    new_mobile = get_valid_input(f"New Mobile (Current: {record_to_update['mobile']}): ", 'mobile', record_to_update['mobile'])

    if (new_name == record_to_update['name'] and 
        new_email == record_to_update['email'] and 
        new_mobile == record_to_update['mobile']):
        
        print(f"{YELLOW}No changes were made to record ID {update_id}.{RESET}")
        return
        
    update_query = "UPDATE user SET name = %s, email = %s, mobile = %s WHERE id = %s"
    db_cursor.execute(update_query, (new_name, new_email, new_mobile, update_id))
    db_connection.commit()
    print(f"{GREEN}Record ID {update_id} updated successfully!{RESET}")

def run_application():
    while True:
        user_input = input(MAIN_MENU_PROMPT).strip()
        operation = MENU_CHOICES.get(user_input)
        
        if not operation:
            print(f'{RED}Please enter a valid menu number (1-4).{RESET}')
            continue
            
        if operation == 'INSERT':
            handle_insert()
        elif operation == 'UPDATE':
            handle_update()
        elif operation == 'DELETE':
            handle_delete()
        elif operation == 'SELECT':
            handle_select()
            
run_application()
