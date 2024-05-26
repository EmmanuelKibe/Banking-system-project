import csv

class Customer:
    def __init__(self, name, account_number, pin, balance):
        # Initialize a Customer object with name, account number, pin, and balance
        self.name = name
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

class BankSystem:
    def __init__(self, csv_file):
        # Initialize a BankSystem object with the path to the CSV file
        self.csv_file = csv_file
        self.customers = self.load_customers()

    def load_customers(self):
        # Load customers from the CSV file and return a list of Customer objects
        customers = []
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                name, account_number, pin, balance = row
                customers.append(Customer(name, account_number, pin, float(balance)))
        return customers

    def find_customer_by_account(self, account_number):
        # Find and return a customer by their account number
        for customer in self.customers:
            if customer.account_number == account_number:
                return customer
        return None

    def save_customers(self):
        # Save the list of customers back to the CSV file
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "account_number", "pin", "balance"])  # Write header row
            for customer in self.customers:
                writer.writerow([customer.name, customer.account_number, customer.pin, customer.balance])

    def validate_pin(self, customer, pin):
        # Validate the customer's PIN with up to 2 attempts
        for _ in range(2):  # Allow up to 2 attempts
            if customer.pin == pin:
                return True
            else:
                pin = input("Incorrect PIN. Please try again: ")
        return False

    def deposit_money(self, account_number, pin, deposit):
        # Deposit money into a customer's account
        customer = self.find_customer_by_account(account_number)
        if customer:
            if self.validate_pin(customer, pin):
                customer.balance += float(deposit)
                self.save_customers()
                return f"You have successfully deposited ${deposit}. Balance for account {account_number}: ${customer.balance:.2f}"
            else:
                return "Your account has been blocked temporarily, since you have reached the maximum number of pin input trials!\nContact the bank through its official communication channels for further assistance."
        else:
            return "Wrong account number!"
        
    def withdraw_money(self, account_number, pin, withdraw):
        # Withdraw money from a customer's account
        customer = self.find_customer_by_account(account_number)
        if customer:
            if self.validate_pin(customer, pin):
                if customer.balance >= float(withdraw):
                    customer.balance -= float(withdraw)
                    self.save_customers()
                    return f"You have successfully withdrawn ${withdraw}. Balance for account {account_number}: ${customer.balance:.2f}"
                else:
                    return f"You have insufficient balance to complete this transaction! Your balance is ${customer.balance:.2f}"
            else:
                return "Your account has been blocked temporarily, since you have reached the maximum number of pin input trials!\nContact the bank through its official communication channels for further assistance."
        else:
            return "Wrong account number!"
        
    def send_money(self, recipient_account, account_number, pin, money_sent):
        # Send money from one customer's account to another's
        customer = self.find_customer_by_account(account_number)
        recipient = self.find_customer_by_account(recipient_account)
        if customer:
            if recipient:
                if self.validate_pin(customer, pin):
                    if customer.balance >= float(money_sent):
                        customer.balance -= float(money_sent)
                        recipient.balance += float(money_sent)
                        self.save_customers()
                        return f"You have sent ${money_sent} to account number {recipient_account}. Balance for {account_number}: ${customer.balance:.2f}"
                    else:
                        return f"You have insufficient balance to complete this transaction! Your balance is ${customer.balance:.2f}"
                else:
                    return "Your account has been blocked temporarily, since you have reached the maximum number of pin input trials!\nContact the bank through its official communication channels for further assistance."
            else:
                return "The account entered does not exist!"
        else:
            return "Wrong account number!"
        
    def create_new_account(self, name, account_number, confirm_account_number, pin, confirm_pin, initial_deposit):
        # Create a new account for a customer
        customer = self.find_customer_by_account(account_number)
        if customer:
            return "This account already exists!"
        else:
            if name:
                if confirm_account_number != account_number:
                    raise ValueError('The account numbers provided do not match. Please try again!')
                
                if confirm_pin != pin:
                    raise ValueError('The pin numbers provided do not match. Please try again!')
                
                if float(initial_deposit) < 0:
                    raise ValueError('The initial deposit must be a positive amount!')
                
            else:
                return "No name was entered!"
        
        new_customer = Customer(name, account_number, pin, float(initial_deposit))
        self.customers.append(new_customer)
        self.save_customers()
        return f"Account created successfully! Your balance is ${float(initial_deposit):.2f}"

    def check_balance(self, account_number, pin):
        # Check the balance of a customer's account
        customer = self.find_customer_by_account(account_number)
        if customer:
            if self.validate_pin(customer, pin):
                return f"Balance for account {account_number}: ${customer.balance:.2f}"
            else:
                return "Your account has been blocked temporarily, since you have reached the maximum number of pin input trials!\nContact the bank through its official communication channels for further assistance."
        else:
            return "Wrong account number!"

# Example usage
if __name__ == "__main__":
    bank_system = BankSystem('customers.csv') 
    
    while True:
        print("\nBank System Menu:")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Send money")
        print("4. Check balance")
        print("5. Create a new account")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = input("Enter your account number: ")

            if not bank_system.find_customer_by_account(account_number):
                print("Wrong account number!")
                break

            pin = input("Enter your PIN: ")
            deposit = input("Enter the amount you wish to deposit: ")
            print(bank_system.deposit_money(account_number, pin, deposit))
            print("\nThank you for using the bank system.")
            break
            
        elif choice == '2':
            account_number = input("Enter your account number: ")

            if not bank_system.find_customer_by_account(account_number):
                print("Wrong account number!")
                break

            pin = input("Enter your PIN: ")
            withdraw = input("Enter the amount you would like to withdraw: ")
            print(bank_system.withdraw_money(account_number, pin, withdraw))
            print("\nThank you for using the bank system.")
            break
        
        elif choice == '3':
            account_number = input("Enter your account number: ")

            if not bank_system.find_customer_by_account(account_number):
                print("Wrong account number!")
                break

            recipient_account = input("Enter account number you wish to send money to: ")

            if not bank_system.find_customer_by_account(recipient_account):
                print("The specified account does not exist")
                break

            pin = input("Enter your PIN: ")
            money_sent = input("Enter amount: ")
            print(bank_system.send_money(recipient_account, account_number, pin, money_sent))
            break

        elif choice == '4':
            account_number = input("Enter your account number: ")

            if not bank_system.find_customer_by_account(account_number):
                print("Wrong account number!")
                break

            pin = input("Enter your PIN: ")
            print(bank_system.check_balance(account_number, pin))
            print("\nThank you for using the bank system.\n")
            break

        elif choice == '5':
            print("Welcome to the banking system. Here, you will create your account as a first time user!\n")
            name = input("Please enter your full names, each name separated by a blank space: ")
            account_number = input("Enter any 6 digit number as your account number: ")
            confirm_account_number = input("Confirm your account number: ")

            if bank_system.find_customer_by_account(account_number):
                print("This account already exists!")
                continue

            pin = input("Enter your four character PIN: ")  
            confirm_pin = input("Confirm your PIN: ")  
            initial_deposit = input("Enter your initial deposit amount: ")
            print(bank_system.create_new_account(name, account_number, confirm_account_number, pin, confirm_pin, initial_deposit))
            print("\nThank you for using the bank system.")
            break

        elif choice == '6':
            print("\nThank you for using the bank system.")
            break
        
        else:
            print("\nInvalid choice. Please try again!")
