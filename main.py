import streamlit as st
from datetime import datetime

# Bank Account class
class BankAccount:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(
                {"type": "Deposit", "amount": amount, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            )
            return f"Successfully deposited: {amount}."
        return "Amount must be greater than zero."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(
                {"type": "Withdrawal", "amount": amount, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            )
            return f"Successfully withdrew: {amount}."
        elif amount > self.balance:
            return "Insufficient funds."
        return "Amount must be greater than zero."

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history


# Store default accounts here
if "accounts" not in st.session_state:
    st.session_state.accounts = {
        "Peter": BankAccount("Peter", "2002", 1500),
        "Billy": BankAccount("Billy", "1980", 1500),
    }
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_account" not in st.session_state:
    st.session_state.current_account = None


# Login interface
if not st.session_state.logged_in:
    st.title("ATM Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Validate username and password
        if username in st.session_state.accounts:
            account = st.session_state.accounts[username]
            if account.password == password:
                st.session_state.logged_in = True
                st.session_state.current_account = account
                st.success(f"Welcome, {username}!")
            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")
else:
    st.sidebar.title("Main Menu")
    option = st.sidebar.selectbox("Select an option:", ["View Balance", "Deposit", "Withdraw", "Transaction History", "Logout"])

    account = st.session_state.current_account

    if option == "View Balance":
        # Display the current balance
        st.title("Your Balance")
        st.write(f"Current balance: {account.get_balance()}.")

    elif option == "Deposit":
        # Deposit interface
        st.title("Deposit")
        amount = st.number_input("Enter amount to deposit:", min_value=0.0, step=0.01)
        if st.button("Deposit"):
            message = account.deposit(amount)
            st.success(message)

    elif option == "Withdraw":
        # Withdraw interface
        st.title("Withdraw")
        amount = st.number_input("Enter amount to withdraw:", min_value=0.0, step=0.01)
        if st.button("Withdraw"):
            message = account.withdraw(amount)
            if "Successfully withdrew" in message:
                st.success(message)
            else:
                st.error(message)

    elif option == "Transaction History":
        # Display transaction history
        st.title("Transaction History")
        transactions = account.get_transaction_history()
        if transactions:
            for transaction in transactions:
                st.write(f"{transaction['time']} - {transaction['type']}: {transaction['amount']}")
        else:
            st.write("No transactions found.")

    elif option == "Logout":
        # Logout
        st.session_state.logged_in = False
        st.session_state.current_account = None
        st.success("Logged out successfully.")
