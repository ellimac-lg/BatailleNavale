

import random

# Initialize the game boards
user_board = [["O"] * 10 for _ in range(10)]
computer_board = [["O"] * 10 for _ in range(10)]

# Place the user's ships on the board
def place_user_ships():
    for i in range(3):
        print("Navire", i+1, ":")
        size = int(input("Entrez la taille du navire (2-5) : "))
        orientation = input("Entrez l'orientation du navire (horizontal ou vertical) : ")
        row = input("Entrez la ligne (A-J) : ")
        col = int(input("Entrez la colonne (1-10) : "))
        if orientation == "horizontal":
            for j in range(size):
                user_board[ord(row) - 65][col + j - 1] = "S"
        else:
            for j in range(size):
                user_board[ord(row) - 65 + j][col - 1] = "S"

# Place the computer's ships on the board randomly
def place_computer_ships():
    for i in range(3):
        size = random.randint(2, 5)
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            row = random.randint(0, 9)
            col = random.randint(0, 10 - size)
            for j in range(size):
                computer_board[row][col + j] = "S"
        else:
            row = random.randint(0, 10 - size)
            col = random.randint(0, 9)
            for j in range(size):
                computer_board[row + j][col] = "S"

# Start the game
place_user_ships()
place_computer_ships()

while True:
    # User's turn
    print("Grille du joueur User ")
    for row in user_board:
        print(" ".join(row))
    row = input("Entrez la ligne (A-J) : ")
    col = int(input("Entrez la colonne (1-10) : "))
    if computer_board[ord(row) - 65][col - 1] == "S":
        print("Vous avez touché un navire de l'ordinateur !")
        computer_board[ord(row) - 65][col - 1] = "X"
    elif computer_board[ord(row) - 65][col - 1] == "X":
        print("Vous avez déjà attaqué cette position !")
    else:
        print("Vous avez raté l'attaque !")
        computer_board[ord(row) - 65][col - 1] = "O"

    # Check if the user has won
    if all(cell != "S" for row in computer_board for cell in row):
        print("Vous avez gagné ! Félicitations !")
        break

    # Computer's turn
    row = random.randint(0, 9)
    col = random.randint(0, 9)
    if user_board[row][col] == "S":
        print("L'ordinateur a touché un de vos navires !")
        user_board[row][col] = "X"
    elif user_board[row][col] == "X":
        print("L'ordinateur a déjà attaqué cette position !")
    else:
        print("L'ordinateur a raté l'attaque !")
        user_board[row][col] = "O"

    # Check if the computer has won
    if all(cell != "S" for row in user_board for cell in row):
        print("Vous avez perdu ! Dommage !")
        break

