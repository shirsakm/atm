import config
import os
from colorama import Fore, Back, Style
from getpass import getpass
from mysql.connector import connect

clear = lambda : os.system('cls')

def main():
    connection = connect(
        host="localhost",
        user="root",
        password="redhat6",
        database="ATM"
    )
    
    mode = get_mode()
    if mode == 0:
        user(connection)
    else:
        admin()


def get_mode():
    import keyboard
    
    term = ["Choose a mode: \n", "[*]", "User\n", Fore.RED, "[ ]", "Admin", Style.RESET_ALL]
    
    clear()
    print(''.join(term))
    while True:
        if keyboard.is_pressed('enter'):
            clear()
            if term[1][1] == '*':
                return 0
            else:
                return 1
                
        if keyboard.is_pressed('down'):
            if term[1][1] == '*':
                term[1] = '[ ]'
                term[4] = '[*]'
                
                clear()
                print(''.join(term))
            
        if keyboard.is_pressed('up'):
            if term[4][1] == '*':
                term[4] = '[ ]'
                term[1] = '[*]'
                
                clear()
                print(''.join(term))
    

def admin():
    creds = get_creds('admin')


def user(conn):
    input(); clear() # This is a weird fix IDK what is wrong
    creds = get_creds('user')

    cursor = conn.cursor()

    query = "SELECT cardno, pin FROM card"

    cursor.execute(query)
    print(cursor.fetchall())

    # Check if card exists

    # Offer options to the user such as "Withdraw, Check Balance"


def get_creds(user: str):
    if user == "user":
        card_no = input("Card No: ")
        pin = getpass("Pin: ")

        # Add a check if the pin is 4 digits and account number is 11 digits
        
        return (card_no, pin)
    
    elif user == "admin":
        return None


if __name__ == '__main__':
    main()
    