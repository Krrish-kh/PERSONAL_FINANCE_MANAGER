import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import hashlib

conn = sqlite3.connect('budget_management.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        savings_goal REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS incomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        income_amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        expense_amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    hashed_password = hash_password(password)
    
    cursor.execute("INSERT INTO users (username, password, savings_goal) VALUES (?, ?, ?)", (username, hashed_password, 0))
    conn.commit()
    print("Account created successfully.")
    return username

def fetch_recent_users():
    cursor.execute("SELECT username FROM users WHERE username != '' ORDER BY id DESC LIMIT 3")
    return cursor.fetchall()

def update_recent_users(username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute("UPDATE users SET id = id WHERE username = ?", (username,))
    else:
        cursor.execute("INSERT INTO users (username, password, savings_goal) VALUES (?, '', 0)", (username,))
    conn.commit()

def remove_recent_user(username):
    cursor.execute("DELETE FROM recent_logins WHERE username = ?", (username,))
    conn.commit()
    print("User removed from recent logins.")
    
def forgot_password():
    username = input("Enter your username: ")
    
    # Check if the username exists in the database
    cursor.execute("SELECT security_question FROM users WHERE username = ?", (username,))
    security_question = cursor.fetchone()
    
    if security_question:
        # Fetch the security question
        security_question = security_question[0]
        
        # Ask the security question
        user_answer = input(f"Security Question: {security_question}\nEnter your answer: ")
        
        # Fetch the answer from the database
        cursor.execute("SELECT security_answer FROM users WHERE username = ?", (username,))
        stored_answer = cursor.fetchone()[0]
        
        # Compare the provided answer with the stored one
        if user_answer.lower() == stored_answer.lower():
            new_password = input("Enter your new password: ")
            hashed_password = hash_password(new_password)
            
            # Update the password in the database
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
            print("Password reset successfully.")
        else:
            print("Incorrect answer to the security question. Please try again.")
    else:
        print("Username not found.")

def login(recent_users):
    while True:
        print("\nRecent Logins:")
        for i, user in enumerate(recent_users, start=1):
            print(f"{i}. {user}")

        choice = input("Enter the number or username to login, or press Enter to login normally: ")

        if choice.isdigit() and int(choice) in range(1, len(recent_users) + 1):
            username = recent_users[int(choice) - 1][0]  # Extract the username from the tuple
        elif choice in [user[0] for user in recent_users]:
            username = choice
        else:
            username = input("Enter your username: ")

        password = input("Enter your password: ")
        hashed_password = hash_password(password)
        
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and hashed_password == user[1]:
            update_recent_users(username)  # Update the recent logins list
            return username, user[0]
        else:
            print("Incorrect username or password.")
            forgot_option = input("Forgot your password? Enter 'yes' to reset or press Enter to try again: ")
            if forgot_option.lower() == "yes":
                forgot_password()  # Call the forgot password function
                continue  # Return to login after attempting password reset

        
def add_income(username, user_id):
    amount = float(input("Enter the amount of income: "))
    cursor.execute("INSERT INTO incomes (user_id, income_amount) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    print("Income added successfully.")

def add_expense(username, user_id):
    amount = float(input("Enter the amount of expense: "))
    purpose = input("Enter the purpose of this expense: ")
    cursor.execute("INSERT INTO expenses (user_id, expense_amount, purpose) VALUES (?, ?, ?)", (user_id, amount, purpose))
    conn.commit()
    print("Expense added successfully.")


def view_expenses(username, user_id):
    cursor.execute("SELECT expense_amount FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    print(f"{username}'s Expenses:")
    for i, expense in enumerate(expenses, start=1):
        print(f"{i}. ${expense[0]}")

def set_savings_goal(username, user_id):
    savings_goal = float(input("Enter your savings goal: "))
    cursor.execute("UPDATE users SET savings_goal = ? WHERE id = ?", (savings_goal, user_id))
    conn.commit()
    print("Savings goal set successfully.")

def check_savings(username, user_id):
    cursor.execute("SELECT SUM(income_amount) FROM incomes WHERE user_id = ?", (user_id,))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(expense_amount) FROM expenses WHERE user_id = ?", (user_id,))
    total_expense = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT savings_goal FROM users WHERE id = ?", (user_id,))
    savings_goal = cursor.fetchone()[0] or 0
    
    total_savings = total_income - total_expense
    savings_percentage = (total_savings / savings_goal) * 100 if savings_goal else 0

    print(f"Total savings: ${total_savings}")
    print(f"Savings goal: ${savings_goal}")
    print(f"Savings percentage: {savings_percentage}%")

def view_donut_chart(username, user_id):
    cursor.execute("SELECT SUM(expense_amount) FROM expenses WHERE user_id = ?", (user_id,))
    total_expense = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(income_amount) FROM incomes WHERE user_id = ?", (user_id,))
    total_income = cursor.fetchone()[0] or 0
    
    labels = ['Expenses', 'Savings']
    sizes = [total_expense, total_income - total_expense]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['red', 'green'], wedgeprops={'edgecolor': 'gray'})
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Expenses vs Savings')
    plt.show()

def view_savings_bar_chart(username, user_id):
    cursor.execute("SELECT SUM(income_amount) FROM incomes WHERE user_id = ?", (user_id,))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(expense_amount) FROM expenses WHERE user_id = ?", (user_id,))
    total_expense = cursor.fetchone()[0] or 0
    
    total_savings = total_income - total_expense
    
    categories = ['Savings']
    values = [total_savings]
    
    plt.figure(figsize=(6, 6))
    plt.bar(categories, values, color='blue')
    plt.title('Total Savings')
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.show()

def view_income_expense_graph(username, user_id):
    # Fetch data for income and expenses
    cursor.execute("SELECT SUM(income_amount) FROM incomes WHERE user_id = ?", (user_id,))
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(expense_amount) FROM expenses WHERE user_id = ?", (user_id,))
    total_expense = cursor.fetchone()[0] or 0

    # Plotting the graph
    labels = ['Income', 'Expense']
    values = [total_income, total_expense]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['blue', 'red'])
    plt.title('Income vs Expense')
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.show()

def view_all_graphs(username, user_id):
    view_income_expense_graph(username, user_id)
    view_donut_chart(username, user_id)
    view_savings_bar_chart(username, user_id)

def view_full_report(username, user_id):
    print("\nBudget Report")
    print("=============")
    cursor.execute("SELECT income_amount FROM incomes WHERE user_id = ?", (user_id,))
    incomes = cursor.fetchall()
    print(f"{username}'s Incomes:")
    for i, income in enumerate(incomes, start=1):
        print(f"{i}. ${income[0]}")
    
    view_expenses(username, user_id)
    check_savings(username, user_id)
    view_all_graphs(username, user_id)

def delete_user(username, user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    print("User deleted successfully.")
    remove_recent_user(username)  # Remove the deleted user from recent logins list


def logout():
    print("Logged out.")

def working_menu(username, user_id):
    while True:
        print("\nWorking Menu")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Expenses")
        print("4. Set Savings Goal")
        print("5. Check Savings")
        print("6. View Income Expense Saving Graph")
        print("7. View Report")
        print("8.Latest Finance Updates")
        print("9. Logout")
        print("10. Delete User")
        option = input("Enter the number of your option: ")

        if option == "1":
            add_income(username, user_id)
        elif option == "2":
            add_expense(username, user_id)
        elif option == "3":
            view_expenses(username, user_id)
        elif option == "4":
            set_savings_goal(username, user_id)
        elif option == "5":
            check_savings(username, user_id)
        elif option == "6":
            view_all_graphs(username, user_id)
        elif option == "7":
            view_full_report(username, user_id)
        elif option == "8":  # New option for Information Menu
            # Redirect to financial education website
            print("Redirecting to the Financial Times Website...")
            import webbrowser
            webbrowser.open("https://www.ft.com")
        elif option == "9":
            logout()
            return
        elif option == "10":
            delete_user(username, user_id)
            return
        else:
            print("Invalid option. Please try again")

def interface_menu():
    while True:
        print("\nInterface Menu")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        option = input("Enter the number of your option: ")

        if option == "1":
            username = sign_up()
            if username:
                print("Returning to the Interface Menu...")
                continue
        elif option == "2":
            recent_users = fetch_recent_users()
            if not recent_users:
                print("No recent usernames available.")
                continue
            username, user_id = login(recent_users)
            if username:
                print("Returning to the Interface Menu...")
        elif option == "3":
            exit()
        else:
            print("Invalid option. Please try again.")

        if username:
            working_menu(username, user_id)
if __name__ == "__main__":
    interface_menu()
