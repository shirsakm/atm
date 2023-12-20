import config
import getpass
import os
from colorama import Fore, Back, Style
from mysql.connector import connect

clear = lambda : os.system('cls')

def main():
    connection = connect(
        host="localhost",
        user="root",
        password="redhat6"
    )
    
    mode = get_mode()
    if mode == 0:
        user()
    else:
        admin()
    
def get_mode():
    import keyboard
    
    term = ["Choose a mode: \n", "[*]", "User\n", Fore.RED, "[ ]", "Admin", Style.RESET_ALL]
    mode = 0
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


def user():
    creds = get_creds('user')
    

def get_creds(user: str):
    if user == "user":
        acc_no = input("ATM No:")
        
        print(acc_no)
        return (acc_no,)
    elif user == "admin":
        return None


if __name__ == '__main__':
    main()
    