import unittest
#from unittest.mock import patch
import os
import csv
from bank_sys import Customer, BankSystem

class TestCustomer(unittest.TestCase):
    def test_customer_attributes(self):
        # Test if Customer attributes are initialized correctly
        customer = Customer("John Doe", "123456", "1234", 1000)
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.account_number, "123456")
        self.assertEqual(customer.pin, "1234")
        self.assertEqual(customer.balance, 1000)

class TestBankSystem(unittest.TestCase):
    # Define the setUp method to prepare for testing
    def setUp(self):
        # Create a temporary CSV file for testing
        self.test_csv_file = 'test_customers.csv'
        with open(self.test_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "account_number", "pin", "balance"])
            writer.writerow(["John Doe", "123456", "1234", "1000"])
            writer.writerow(["Jane Smith", "654321", "4321", "2000"])

    # Define the tearDown method to clean up after testing
    def tearDown(self):
        # Remove the temporary CSV file
        os.remove(self.test_csv_file)

    def test_deposit_money(self):
        # Test depositing money into an account
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.deposit_money("123456", "1234", "500")
        self.assertEqual(result, "You have successfully deposited $500. Balance for account 123456: $1500.00")

    def test_withdraw_money_insufficient_balance(self):
        # Test withdrawing money with insufficient balance
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.withdraw_money("123456", "1234", "1500")
        self.assertEqual(result, "You have insufficient balance to complete this transaction! Your balance is $1000.00")

    def test_withdraw_money(self):
        # Test withdrawing money from an account
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.withdraw_money("123456", "1234", "500")
        self.assertEqual(result, "You have successfully withdrawn $500. Balance for account 123456: $500.00")

    def test_send_money_invalid_recipient(self):
        # Test sending money to an invalid recipient account
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.send_money("999999", "123456", "1234", "500")
        self.assertEqual(result, "The account entered does not exist!")

    def test_send_money_insufficient_balance(self):
        # Test sending money with insufficient balance
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.send_money("654321", "123456", "1234", "1500")
        self.assertEqual(result, "You have insufficient balance to complete this transaction! Your balance is $1000.00")

    def test_send_money(self):
        # Test sending money to another account
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.send_money("654321", "123456", "1234", "500")
        self.assertEqual(result, "You have sent $500 to account number 654321. Balance for 123456: $500.00")

    def test_create_new_account(self):
        # Test creating a new account
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.create_new_account("Alice Wonderland", "111111", "111111", "5678", "5678", "100")
        self.assertEqual(result, "Account created successfully! Your balance is $100.00")

    def test_check_balance(self):
        # Test checking the balance of an account
        bank_system = BankSystem(self.test_csv_file)
        result = bank_system.check_balance("123456", "1234")
        self.assertEqual(result, "Balance for account 123456: $1000.00")

    def test_find_customer_by_account(self):
        # Test finding a customer by account number
        bank_system = BankSystem(self.test_csv_file)
        customer = bank_system.find_customer_by_account("123456")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.pin, "1234")
        self.assertEqual(customer.balance, 1000)

if __name__ == '__main__':
    unittest.main()
