import bcrypt
import random
import pwinput
import sqlite3
import os
import time
import sys
# import main

def exit():
    if  (int(input("Exit? (0): "))) == 1:
        print("Exit")
    # main()

def cls(sts):
    # Cls
    os.system('cls' if os.name == 'nt' else 'clear')

    done = 'false'
    # Loading animation
    def animate(sts):
        while done == (sts):
            sys.stdout.write('\rloading |')
            time.sleep(0.1)
            sys.stdout.write('\rloading /')
            time.sleep(0.1)
            sys.stdout.write('\rloading -')
            time.sleep(0.1)
            sys.stdout.write('\rloading \\')
            time.sleep(0.1)
        sys.stdout.write('\rDone!     ')

    # animate("false")
    # time.sleep(5)
    # animate(sts)
    # time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')

def create_db():
    # Create Database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')

    conn.commit()
    conn.close()

# Profile update 
def prof_update(prop, username):
    # Clear shell
    cls("true")

    if prop == 1:
        # Ussername update
        print("\n---------------| Profile Update |---------------")
        new_un = (input("Enter the new username you want to update: "))
        print("\n--------------------------------------------------")

        # Update username from the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("UPDATE users SET username=? WHERE username =?", (new_un, username))

        row = c.fetchone()
        print("data: ",row,"\n","new username: ",new_un, "username: ",username)


        if row is not None:
            print("Username updated succesfully !")
            time.sleep(5)
        print("Something is wrong!")
        time.sleep(5)

        conn.close()

    if prop == 2:
         # Ussername update
        print("\n---------------| Profile Update |---------------")
        password = (input("Enter the new password you want to update: "))
        password_check(password)
        print("\n--------------------------------------------------")
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update username from the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("UPDATE users SET password=? WHERE username =?", (hashed_password, username))

        row = c.fetchone()
        time.sleep(5)
        print("data: ",row,"\n","new hashed password: ",hashed_password, "username: ",username)
        
        if row is not None:
            print("Password updated succesfully !")
            time.sleep(5)
        print("Something is wrong!")
        time.sleep(5)

        

        conn.close()

# Profile
def profile(username):
    # Clear shell
    cls("true")

    # Profile
    print("\n---------------| Profile |---------------")
    print("\n> Welcome User: ", username)
    print("\nUpdate username -> (1)")
    print("Update password -> (2)")
    inp = int(input("\nChoice: "))
    prof_update(inp, username)
    print("\n-----------------------------------------")

# Login Fn
def login():
    # Clear shell
    cls("true")

    # Call db function
    create_db()

    print("\n---------------| Login |---------------")

    username = input("> Enter username: ")
    password = pwinput.pwinput("> Enter password: ")


    # Fetch the user's hashed password from the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))

    row = c.fetchone()

    conn.close()
    # print("data: ",row,"\n")

    if row is None:
        print("\nInvalid username or password")
        print("-----------------------------------------\n")
        return

    hashed_password = row[2]

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        print("\n* Login successful!")
        time.sleep(3)
        usernm = row[1]
        profile(usernm)
        return True
    else:
        print("\n* Invalid username or password")
        # exit()
        return False


# Signup Fn
def signup():
    # Clear shell
    cls("true")

    # Signup page
    print("\n---------------| Signup |---------------")

    
    username = input("> Enter username: ")
    password = pwinput.pwinput("> Enter password: ")

    password_check(password)

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Insert the new user into the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

    conn.commit()
    conn.close()

    print("\n* User created successfully!")
    time.sleep(3)
    login()
    return True

# Generate random password
def random_pass(length):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%^&*{}|":>?<'
    password = ''
    for i in range(length):
        password += random.choice(chars)
    # signup()
    return password


# Password checker
def password_check(password):
    # Generate a captcha code
    def generate_captcha():
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        captcha = ''
        for i in range(6):
            captcha += random.choice(chars)
        return captcha

    # Check the strength of a password
    def check_password_strength():
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in '!@#$%^&*()_-+={}[]|\:;"<>,.?/' for c in password):
            strength += 1
        return strength

    # User password validation
    def pass_validation():
        captcha = generate_captcha()
        print("\nPlease enter the following captcha to complete your registration:", captcha)
        captcha_input = input("\nEnter the captcha: ")
        if captcha_input == captcha:
            password_strength = check_password_strength()
            if password_strength == 4:
                print("\n* Your password is very strong!\n")
            elif password_strength == 3:
                print("\n* Your password is strong.\n")
            elif password_strength == 2:
                print("\n* Your password is weak. Please consider adding more complexity.\n")
            else:
                print("\n* Your password is very weak. Please choose a stronger password.\n")
                Yn = input("> Generate a password? (y/n): ")
                if(Yn == "y"):
                    length = int(input("\nEnter the password length you want: "))
                    re_pass = random_pass(int(length))
                    print("\nYour generated password is: ", re_pass)
                    print("\n10 sec count down to copy the password.")
                    time.sleep(10)
                    # for i in range (time.sleep(10)):
                    #     print(i)
            # login()
        else:
            print("* Captcha verification failed. Please try again.")
            print("* Signup again")
            time.sleep(2)
            signup()
        
    pass_validation()
