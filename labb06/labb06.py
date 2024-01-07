import socket

def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server_socket

def http_server(port):
    host = "127.0.0.1"

    server_socket = create_socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server is listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()#accepterar(öppnar dörren) o ger socket (walkietalkie)
        print(f"Connection established with {client_address}")

        request_data = client_socket.recv(1024).decode("ASCII")
        print("Client's Request:\n")
        print(request_data)

        response = "HTTP/1.1 200 OK\n"
        response += "Content-Type: text/html\n\n"
        response += "<html>\n"
        response += "<pre>\n"
        response += "<h1> Your browser sent the following request </h1>"
        response += request_data 
        response += "\n</pre>\n"
        response += "</html>\n"

        # skicka till response client
        client_socket.sendall(bytearray(response, "ASCII"))

        # stänger
        client_socket.close()

if __name__ == "__main__":
    port = 8080

    try:
        http_server(port)
    except KeyboardInterrupt:
        print("Server stopped.")
