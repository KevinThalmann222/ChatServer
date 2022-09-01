"""Kevin Thalmann
"""
import socket
import threading

nickname = input("Choose your Nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.3.164.44", 9090))


def receive():
    """_summary_"""
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except Exception as ex:
            print(f"an error occurred: {ex}")
            client.close()
            break


def write():
    """_summary_"""
    while True:
        message = f"{nickname}: {input('')}".encode("utf-8")
        client.send(message)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
