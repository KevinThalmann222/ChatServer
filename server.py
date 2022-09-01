import socket
import threading

Host = "10.3.164.44"
Port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host, Port))
server.listen()

clients = []
nicknames = []


def broadcast(mgs):
    """_summary_

    Args:
        mgs (_type_): _description_
    """
    for client in clients:
        client.send(mgs)


def handle(client):
    """_summary_

    Args:
        client (_type_): _description_
    """
    while True:
        try:
            mgs = client.recv(1024)
            broadcast(mgs)
        except Exception:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!".encode("utf-8"))
            break


def receive():
    """_summary_"""
    while True:
        client, address = server.accept()
        print(f"connected with: {str(address)}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))
        client.send("Your are connected!".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server is listening ...")
receive()
