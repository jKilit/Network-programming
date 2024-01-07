import socket
import select

PORT = 60003
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", PORT))
server_socket.listen(1)

list_of_sockets = [server_socket]

print("Listening on port {}".format(PORT))

while True:
    readable, _, _ = select.select(list_of_sockets, [], [])
    
    for sock in readable:
        if sock == server_socket:
            (client_socket, client_addr) = server_socket.accept()
            for s in list_of_sockets:
                if s != server_socket:
                    message = "[{}:{}] (connected)".format(client_addr[0], client_addr[1]) #alla clients får om någon är connectad #ip, port
                    s.send(message.encode())
            list_of_sockets.append(client_socket)

        else:
            data = sock.recv(1024)
            if not data:
                client_addr = sock.getpeername()
                print("Client {}:{} disconnected".format(client_addr[0], client_addr[1])) #ip, port
                list_of_sockets.remove(sock)
                sock.close()
                for s in list_of_sockets:
                    if s != server_socket:
                        message = "[{}:{}] (disconnected)".format(client_addr[0], client_addr[1])
                        s.send(message.encode())
            else:
                sender_addr = sock.getpeername()
                message = "[{}:{}] {}".format(sender_addr[0], sender_addr[1], data.decode())
                for s in list_of_sockets:
                    if s != server_socket:
                        s.send(message.encode())
