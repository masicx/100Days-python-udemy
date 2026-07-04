"""
Tic Tac Toe - Juego de Triqui para dos jugadores
Ejecutar con: python tic_tac_toe.py
"""

def create_board():
    return [" " for _ in range(9)]


def show_board(board):
    print()
    print(f"  {board[0]} | {board[1]} | {board[2]} ")
    print(" ___|___|___")
    print(f"  {board[3]} | {board[4]} | {board[5]} ")
    print(" ___|___|___")
    print(f"  {board[6]} | {board[7]} | {board[8]} ")
    print("    |   |   ")
    print()


def show_positions():
    print("Posiciones del tablero (usa estos numeros para jugar):")
    print()
    print("  1 | 2 | 3 ")
    print(" ___|___|___")
    print("  4 | 5 | 6 ")
    print(" ___|___|___")
    print("  7 | 8 | 9 ")
    print("    |   |   ")
    print()


WINNER_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
    (0, 4, 8), (2, 4, 6),             # diagonales
]


def is_winner(board, ficha):
    return any(
        board[a] == board[b] == board[c] == ficha
        for a, b, c in WINNER_COMBINATIONS
    )


def board_is_full(board):
    return all(casilla != " " for casilla in board)


def ask_movement(board, jugador):
    while True:
        entry = input(f"Jugador {jugador}, elige una posicion (1-9): ").strip()
        if not entry.isdigit():
            print("Por favor ingresa un numero del 1 al 9.")
            continue
        position = int(entry) - 1
        if position < 0 or position > 8:
            print("Numero fuera de rango. Elige entre 1 y 9.")
            continue
        if board[position] != " ":
            print("Esa casilla ya esta ocupada. Elige otra.")
            continue
        return position


def play():
    print("=" * 30)
    print("   TIC TAC TOE - TRIQUI")
    print("=" * 30)
    show_positions()

    board = create_board()
    fichas = {1: "X", 2: "O"}
    turn = 1

    while True:
        show_board(board)
        ficha = fichas[turn]
        position = ask_movement(board, turn)
        board[position] = ficha

        if is_winner(board, ficha):
            show_board(board)
            print(f"¡Jugador {turn} ({ficha}) ha ganado! 🎉")
            break

        if board_is_full(board):
            show_board(board)
            print("¡Empate! Nadie gano esta vez.")
            break

        turn = 2 if turn == 1 else 1

    play_again = input("\n¿Quieres jugar de nuevo? (s/n): ").strip().lower()
    if play_again == "s":
        play()
    else:
        print("¡Gracias por jugar!")


if __name__ == "__main__":
    play()