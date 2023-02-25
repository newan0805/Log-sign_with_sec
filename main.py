import os
from fn import login, signup

def main():
    # Cls shell
    os.system('cls' if os.name == 'nt' else 'clear')

    # Call select page
    print("------------| Page |------------")
    print("> Login -> (1)")
    print("> Signup -> (2)")
    sel = int(input("\nSelect: "))
    if sel == 1:
        login()
    if sel == 2:
        signup()
    print("----------------------------------")
    main()

main()