class Customer:
    def __init__(self, customer_number, name, surname):
        self.customer_number = customer_number
        self.name = name
        self.surname = surname

    def show_info(self):
        print(50 * "#")
        print(f"""Customer Information:
        Name: {self.name}
        Surname: {self.surname}
        Customer Number: {self.customer_number}
        """)


class Account:
    def __init__(self, account_number, customer, balance = 0):
        self.account_number = account_number
        self.customer = customer
        self.balance = balance
        self.accountActivity = True

    def deposit_money(self, amount):
        if self.accountActivity and amount > 0:
            self.balance += amount
            print(f"""
                Amount you deposited: {amount}
                New Balance: {self.balance}
            """)
        elif not self.accountActivity:
            print("Your account is not active.")

        else:
            print("The number you have entered is incorrect, please try again.")

    def withdraw_money(self, amount):
        if self.accountActivity and amount <= self.balance:
            self.balance -= amount
            print(f"""
                Amount you withdrawed: {amount}
                New Balance: {self.balance}
            """)
        elif not self.accountActivity:
            print("The account is currently closed.")
        elif amount > self.balance:
            print(f"The amount you entered {amount} is greater than your bank balance {self.balance}, please try again.")
        else:
            print("The amount you have entered is incorrect.")

    def check_balance(self):
        if self.accountActivity:
            print(f"Your bank balance: {self.balance}")
        else:
            print("Your account is inactive.")

    def activate_account(self):
        if not self.accountActivity:
            self.accountActivity = True
            print("Your account has been activated.")
        else:
            print("Your account is already active.")

    def deactivate_account(self):
        if self.accountActivity:
            self.accountActivity = False
            print("Your account has been deactivated.")
        else:
            print("Your account is already deactive.")

    def show_info(self):
        print(f"\nAccount Information: ")
        print(f"""
            Account Number : {self.account_number}
            Account Balance: {self.balance}
        """)
        customer.show_info()


class Bank:
    def __init__(self):
        self.accounts = []
        self.customers = []

    def create_account(self, customer, first_balance = 0):
        account_number = len(self.accounts) + 100
        account = Account(account_number, Customer, first_balance)
        self.accounts.append(account)
        print(f"{account_number} numbered account has been created successfully.")

    def all_accounts(self):
        print("\nAll Accounts: ")
        for account in self.accounts:
            account.show_info()

    def all_customers(self):
        print("\nAll Customers: ")
        for customer in self.customers:
            customer.show_info()

    def account_number_check(self):
        account_number = int(input("Enter your account number: "))
        account = next((account for account in bank.accounts if account.account_number == account_number), None)
        if account:
            return account
        else:
            print("Account has not been found.")
            return None


bank = Bank()


while True:
    print(20 * "*", "Bank Management System", 20 * "*")
    print("""
        1. Open Account
        2. All Accounts List
        3. All Customers List
        4. Deposit Money
        5. Withdraw Money
        6. Check Balance
        7. Deactivate Account
        8. Activate Account
        9. Exit    
    """)

    action = input("Select the action you wanted to perform: ")

    if action == "1":
        customer_number = input("Enter the account number: ")
        name = input("Name: ")
        surname = input("Surname: ")
        customer = Customer(customer_number, name, surname)
        bank.customers.append(customer)
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
        print("You are exiting the system...")
        break

    else:
        print("You have entered a wrong command, please try again.")









