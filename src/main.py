import config
import getpass
import keyboard
import os
from colorama import Fore, Back, Style
from mysql.connector import connect


def main():
    connection = connect(
        host="localhost",
        user="root",
        password="redhat6"
    )
    
    mode()
    
def mode():
    term = ["Choose a mode: \n", "[*]", "User\n", Fore.RED, "[ ]", "Admin", Style.RESET_ALL]
    print(''.join(term))
    while True:
        if keyboard.is_pressed('enter'):
            os.system('cls')
            if term[1][1] == '*':
                user()
            else:
                admin()
                
        if keyboard.is_pressed('down'):
            if term[1][1] == '*':
                term[1] = '[ ]'
                term[4] = '[*]'
                
                os.system('cls')
                print(''.join(term))
            
        if keyboard.is_pressed('up'):
            if term[4][1] == '*':
                term[4] = '[ ]'
                term[1] = '[*]'
                
                os.system('cls')
                print(''.join(term))


def admin():
    exit()


def user():
    pass
     # print(get_creds('user'))


"""
def get_creds(user: str):
    if user == "user":
        acc_no = input("Please enter ATM number: ")
        pin = getpass.getpass(prompt='Pin: ')
        
        return (acc_no, pin)
    elif user == "admin":
        pass
"""


if __name__ == '__main__':
    main()
    