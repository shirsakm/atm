import os
import random
from colorama import Fore, Back, Style
from getpass import getpass
from mysql.connector import connect, MySQLConnection
from dotenv import load_dotenv

load_dotenv()

clear = lambda : os.system('cls')

def main():
    connection = connect(
        host=os.getenv("DB_host"),
        user=os.getenv("DB_user"),
        password=os.getenv("DB_pass"),
        database=os.getenv("DB_name")
    )
    
    mode = get_mode()
    if mode == 0:
        user(connection)
    else:
        admin()


def generate_card_number():
    # Choose a random 15-digit number (the first digit is usually fixed for card types)
    # For example, for Visa, it starts with 4; for Mastercard, it starts with 5, etc.
    card_number = [random.randint(0, 9) for _ in range(15)]

    # Applying Luhn algorithm to create the checksum digit
    total = 0
    for i, digit in enumerate(reversed(card_number)):
        if i % 2 == 0:
            digit *= 2
        if digit > 9:
            digit -= 9
        total += digit

    checksum_digit = (10 - (total % 10)) % 10

    # Return a string representation of the card number
    card_number.append(checksum_digit)
    print("".join(map(str, card_number)))
    return ''.join(map(str, card_number))


def verify_card_number(card_number):
    # Check if the card number is 16 digits
    if len(card_number) != 16:
        return False

    # Check if the card number is all digits
    if not card_number.isdigit():
        return False

    # Check if the card number is valid using luhn algorithm
    total = 0
    check = str(card_number)[len(str(card_number))-1]

    for i, d in enumerate(str(card_number)):
        if i == len(str(card_number))-1:
            break
        d = int(d)
        if(i % 2 == 0):
            d *= 2
        sum = (d)/10 + d%10
        total += sum
        return 10-total%10 == check 


def check_card_exists(card_number, conn: MySQLConnection):
    cursor = conn.cursor()

    query = "SELECT cardno FROM card WHERE cardno = %s"

    cursor.execute(query, (card_number,))

    return cursor.fetchone() is not None


def generate_card(conn: MySQLConnection, accno, pin, name: str|None):
    card_number = generate_card_number()

    cursor = conn.cursor()

    query = "INSERT INTO cards (cardno, accno, pin, name) VALUES (%s, %s, %s, %s)" if name else "INSERT INTO card (cardno, accno, pin) VALUES (%s, %s, %s)"
    params = (card_number, accno, pin, name) if name else (card_number, accno, pin)

    cursor.execute(query, params)

    conn.commit()

    return card_number


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


def transaction(conn: MySQLConnection, card_number: str, amount: int):
    cursor = conn.cursor()

    query = "UPDATE account SET balance = balance - %s WHERE accno = (SELECT accno FROM card WHERE cardno = %s)"
    params = (amount, card_number)

    cursor.execute(query, params)

    conn.commit()


def add_user(conn: MySQLConnection, username):
    cursor = conn.cursor()
    accno = random.randint(1e11, 11111111111*9)
    query = "INSERT INTO user (accno, balance, name) VALUES (%s, %s, %s)"
    params = (accno, 0, username)

    cursor.execute(query, params)
    return accno


def admin():
    creds = get_creds('admin')


def user(conn: MySQLConnection):
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

        # Add a check if the pin is 4 digits and account number is 11 digits and card is valid
        aok = len(str(card_no)) == 11 and len(str(pin)) == 4
        
        return (card_no, pin) if aok else None
    
    elif user == "admin":
        return None


if __name__ == '__main__':
    main()
    