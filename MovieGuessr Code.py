from os import system, name
import random
import requests

# function to clear terminal
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# function to display instructions
def instructions():
    print('''                          
                                 ***INSTRUCTIONS***
            Computer will choose a random movie and display all the vowels, 
            numbers and special characters present in it..

            You have to guess the movie letter by letter...

            eg. if you enter 'n' then the computer will show you all the
            places where n is present.

            You will get 1 point for each correct guess.

            You can guess a maximum of 5 wrong letters!
            
            After 3 incorrect guesses you will be given a hint ;)

    ''')
    input("press Enter to continue")
    main()

# function to display the movie and score
def display(dis, score):
    clear()
    t = len(dis) + 9
    print("\n")
    print("╔", end='')
    print('═'*t, end='')
    print("╗")
    print("║ MOVIE: ", end="")
    for x in dis:
        print(x, end="")
    print(" ║")
    print("╚", end='')
    print('═'*t, end='')
    print("╝")
    print("\t\t\t\t\t score:", score, '\n')

# game function
def Game(score):
    name = ""
    Rating = 10
    hint = ""
    print("\t\t\tSearching a movie...")
    global use
    while(0 < Rating <= 50):
        page = random.randint(1, 500)
        while(page in use):
            page = random.randint(1, 500)
        use.append(page)
        r = requests.get(
            f'https://api.themoviedb.org/3/movie/popular?api_key=961eac3266854d93b722e893e6485014&language=en-US&page={page}')
        s = []
        sd = {}
        for i in r.json()["results"]:
            try:
                s.append(int(i["popularity"]))
                sd[int(i["popularity"])] = [i["title"], i["release_date"]]
            except KeyError:
                continue

        Rating = int(max(s))
        name = sd[max(s)][0]
        hint = sd[max(s)][1]
    name = list(name.lower())

    ans = []
    for x in name:
        if x in ("aeiou0123456789! $%&'()*+,-./:;<=>?@[\]^_`{|}~¡·"):
            ans.append(x)
        else:
            ans.append("-")
    display(ans, score)

    count = 5
    used = ""
    while True:
        if ans == name:
            score += 1
            display(name, score)
            print(f"Alphabets used: {used}")
            print("CONGRATULATIONS! You guessed it! :) ")
            print('''
                    1. Next movie!
                    2. Restart
                    3. Main menu
            ''')
            while True:
                try: 
                    ch = int(input("Enter your choice: "))
                    if ch == 1:
                        Game(score)
                    elif ch == 2:
                        Game(score=0)
                    elif ch == 3:
                        main()
                    else:
                        print("Enter a valid option!")
                        pass
                except ValueError:
                    print("Enter a valid choice!")
                    continue
        if count <= 2:
            print("\t\tHint(release date of the movie):", hint)

        if count == 0:
            display(name, score)
            print(f"Alphabets used: {used}")
            print("You lost! better luck next time :( ")
            print('''
                    1. Play again
                    2. Main menu
            ''')
            while True:
                try: 
                    ch = int(input("Enter your choice: "))
                    if ch == 1:
                        Game(score=0)
                    elif ch == 2:
                        main()
                    else:
                        print("Enter a valid option!")
                        pass
                except ValueError:
                    print("Enter a valid choice!")
                    continue

        print(f"Alphabets used: {used}")
        print(f"Wrong Attempts Left: {count}")

        check = input("Give an Input (single alphabet only): ")
        while(check == ''):
            check = input("Give Input: ")
        check = check[0].lower()

        if (name.count(check) > 0) and (check.upper() not in used):
            used += check.upper()+" "
            for i, y in enumerate(name):
                if y == check:
                    ans[i] = check

        elif check.upper() not in used:
            used += "(" + check.upper() + ") "
            count -= 1

        display(ans, score)
        print()

# function to display main menu
def main():
    score = 0
    while True:
        clear()
        print('''
             ╔══════════════════════════════╗
             ║        *** WELCOME ***       ║
             ╠══════════════════════════════╣  
             ║1. Play                       ║
             ║2. Instructions               ║
             ║3. Exit                       ║
             ╚══════════════════════════════╝
             ''')
        while True:
            try:
                ch = int(input("Enter your choice: "))
                break
            except ValueError:
                print("\nplease enter an integer!")
                continue
        if ch == 1:
            Game(0)
        elif ch == 2:
            instructions()
        elif ch == 3:
            break
        else:
            print("Enter a valid choice!")
    print("Thank you for playing!")
    exit()

use = []

if __name__ == '__main__':
    main()