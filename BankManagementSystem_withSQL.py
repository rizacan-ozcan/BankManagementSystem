import sqlite3
import random


class Customer:
    def __init__(self, customer_number, name, surname):
        self.customer_number = customer_number
        self.name = name
        self.surname = surname

    def show_info(self):
        print(f"""Customer Information
            Name : {self.name}
            Surname : {self.surname}
            Customer Number : {self.customer_number}
        """)

class Account:
    def __init__(self, account_number, customer, balance = 0):
        self.account_number = account_number
        self.customer = customer
        self.balance = balance
        self.account_activity = True

    def deposit_money(self, amount):
        if self.account_activity and amount > 0:
            self.balance += amount
            self.update_account()
            print(f"""
                Amount you deposited: {amount}
                New Balance: {self.balance}
            """)
        elif not self.account_activity:
            print("Your account is not active.")

        else:
            print("The number you have entered is incorrect, please try again.")

    def withdraw_money(self, amount):
        if self.account_activity and amount <= self.balance:
            self.balance -= amount
            self.update_account()
            print(f"""
                Amount you withdrawed: {amount}
                New Balance: {self.balance}
            """)
        elif not self.account_activity:
            print("The account is currently closed.")
        elif amount > self.balance:
            print(f"The amount you entered {amount} is greater than your bank balance {self.balance}, please try again.")
        else:
            print("The amount you have entered is incorrect.")

    def check_balance(self):
        if self.account_activity:
            print(f"Your bank balance: {self.balance}")
        else:
            print("Your account is inactive.")

    def activate_account(self):
        if not self.account_activity:
            self.account_activity = True
            print("Your account has been activated.")
            self.update_account()
        else:
            print("Your account is already active.")

    def deactivate_account(self):
        if self.account_activity:
            self.account_activity = False
            self.update_account()
            print("Your account has been deactivated.")
        else:
            print("Your account is already deactive.")

    def show_info(self):
        print(f"\nAccount Information: ")
        print(f"""
            Account Number : {self.account_number}
            Account Balance: {self.balance}
        """)
        self.customer.show_info()

    def update_account(self):
        connection = sqlite3.connect('bank.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE ACCOUNTS SET BALANCE = ?, ACCOUNT_ACTIVITY = ? WHERE ACCOUNT_NUMBER = ?', (self.balance, 1 if self.account_activity  else 0, self.account_number))
        connection.commit()
        connection.close()


class Bank:

    def __init__(self):
        self.make_connection()

    def make_connection(self):
        self.connection = sqlite3.connect('bank.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS CUSTOMERS (
                CUSTOMER_NUMBER VARCHAR(11) PRIMARY KEY,
                NAME VARCHAR(100),
                SURNAME VARCHAR(100)
            )
        ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ACCOUNTS (
                ACCOUNT_NUMBER INTEGER PRIMARY KEY AUTOINCREMENT,
                CUSTOMER_NUMBER VARCHAR(11),
                BALANCE REAL,
                ACCOUNT_ACTIVITY BIT,
                FOREIGN KEY (CUSTOMER_NUMBER) REFERENCES CUSTOMERS(CUSTOMER_NUMBER)
            )
        ''')
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def create_account(self, customer, first_balance = 0):
        account_number = random.randint(1000, 9999999)
        account = Account(account_number, customer, first_balance)
        self.save_account(account)
        self.save_customer(customer)
        print(f"{account_number} numbered account has been created.")
        return account

    def save_customer(self, customer):
        self.cursor.execute('INSERT INTO CUSTOMERS VALUES(?, ?, ?)', (customer.customer_number, customer.name, customer.surname))
        self.connection.commit()

    def save_account(self, account):
        self.cursor.execute('INSERT INTO ACCOUNTS VALUES(?, ?, ?, ?)',
    (account.account_number, account.customer.customer_number, account.balance, 1 if account.account_activity else 0))
        self.connection.commit()

    def all_accounts(self):
        print("\nAll Accounts: ")
        self.cursor.execute('SELECT * FROM ACCOUNTS')
        account_rows = self.cursor.fetchall()
        for row in account_rows:
            account_number, customer_number, balance, account_activity = row
            customer = self.customer_check(customer_number)
            account = Account(account_number, customer, balance)
            account.account_activity = True if account_activity == 1 else False
            account.show_info()

    def all_customers(self):
        print("\nAll Customers: ")
        self.cursor.execute('SELECT * FROM CUSTOMERS')
        customer_rows = self.cursor.fetchall()
        for row in customer_rows:
            customer_number, name, surname = row
            customer = Customer(customer_number, name, surname)
            customer.show_info()

    def account_number_check(self):
        account_number = int(input("Enter your account number here: "))
        self.cursor.execute('SELECT * FROM ACCOUNTS WHERE ACCOUNT_NUMBER = ?', (account_number,))
        account_row = self.cursor.fetchone()
        if account_row:
            customer = self.customer_check(account_row[1])
            account = Account(account_row[0], customer, account_row[2])
            Account.account_activity = True if account_row[3] == 1 else False
            return account
        else:
            print("Account could not found.")
            return None

    def customer_check(self, customer_number):
        self.cursor.execute('SELECT * FROM CUSTOMERS WHERE CUSTOMER_NUMBER = ?', (customer_number,))
        customer_row = self.cursor.fetchone()
        if customer_row:
            customer = Customer(customer_row[0], customer_row[1], customer_row[2])
            return customer
        else:
            return None


bank = Bank()


try:
    while True:
        print(20 * "*", "Bank Management System", 20 * "*")
        print("""
            1. Create Account
            2. All Accounts
            3. All Customers
            4. Deposit Money
            5. Withdraw Money
            6. Check Balance
            7. Dectivate Account
            8. Activate Account
            9. Exit
        """)
        action = input("Please enter the action you wanted to perform: ")
        if action == "1":
            customer_number = input("Account number: ")
            name = input("Name: ")
            surname = input("Surname: ")
            customer = Customer(customer_number, name, surname)
            bank.create_account(customer)

        elif action == "2":
            bank.all_accounts()

        elif action == "3":
            bank.all_customers()

        elif action == "4":
            account = bank.account_number_check()
            if account:
                amount = float(input("Enter the amount you wanted to deposit: "))
                account.deposit_money(amount)

        elif action == "5":
            account = bank.account_number_check()
            if account:
                amount = float(input("Enter the amount you wanted to withdraw: "))
                account.withdraw_money(amount)

        elif action == "6":
            account = bank.account_number_check()
            if account:
                account.check_balance()

        elif action == "7":
            account = bank.account_number_check()
            if account:
                account.deactivate_account()

        elif action == "8":
            account = bank.account_number_check()
            if account:
                account.activate_account()

        elif action == "9":
            print("You are exiting the system..."),
            break

        else:
            print("You have entered a wrong command, please try again.")
finally:
    bank.close_connection()





