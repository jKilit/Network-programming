import socket

# Skapar socket
def create_socket():#skapar socket som heter game_socket o returnerar
    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return game_socket

# Settar up server
def server_setup():
    host = "127.0.0.1"  # IP address
    port = 60003 

    server_socket = create_socket()
    server_socket.bind((host, port))#binder ihop host och port
    server_socket.listen(1)  # Lyssnar efter en client

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept() 
    print("Connection established with", client_address)
    return server_socket, client_socket

# Settar up the client
def client_setup(server_ip): 
    port = 60003 

    client_socket = create_socket()
    client_socket.connect((server_ip, port))
    print("Connected to the server")
    return client_socket

def play_game(player_socket):
    player_points = 0
    opponent_points = 0

    while True:
        print(f"({player_points},{opponent_points}) Your move: ", end='')
        player_move = input().strip().upper()

        # Checkar efter valid move
        if player_move not in ["R", "P", "S"]:
            print("Invalid move. Please enter R, P, or S.")
            continue

        player_socket.send(player_move.encode())

        opponent_move = player_socket.recv(1024).decode()
        print(f"(Opponent's move: {opponent_move})")

        # logic
        if (player_move == "R" and opponent_move == "S") or \
           (player_move == "S" and opponent_move == "P") or \
           (player_move == "P" and opponent_move == "R"):
            player_points += 1
        elif (opponent_move == "R" and player_move == "S") or \
             (opponent_move == "S" and player_move == "P") or \
             (opponent_move == "P" and player_move == "R"):
            opponent_points += 1

        if player_points == 10 or opponent_points == 10:
            break

    print("Game over!")
    if player_points > opponent_points:
        print(f"You won {player_points} against {opponent_points}")
    else:
        print(f"You lost with {player_points} against {opponent_points}")

    player_socket.close()

if __name__ == "__main__":
    choice = input("Do you want to be server (S) or client (C): ").strip().upper()

    if choice == "S":
        server_socket, client_socket = server_setup()
        play_game(client_socket)
        server_socket.close()
    elif choice == "C":
        server_ip = input("Enter the server's name or IP: ")
        client_socket = client_setup(server_ip)
        play_game(client_socket)
    else:
        print("Invalid choice. Please enter S or C.")
