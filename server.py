import socket
import threading


class CreateServer:
    def __init__(self, auto_ip: bool = False, port: int = 9090) -> None:
        """Init

        Args:
            auto_ip (bool, optional): read the ip Automatic. Defaults to False.
            port (int, optional): ip Port. Defaults to 9090.
        """
        if auto_ip:
            self.hostname = socket.gethostname()
        else:
            self.hostname = "10.3.164.44"
        self.port = port
        # create a internet port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, self.port))
        # server is listing
        self.server.listen()
        # list of clients and nicknames
        self.clients = []
        self.nicknames = []

    def broadcast(self, mgs: str) -> None:
        """Sends infomations at of clients

        Args:
            mgs (str): message
        """
        for client in self.clients:
            # Send data to the socket. The socket must be connected to a remote socket.
            client.send(mgs)

    def handle(self, client: object) -> None:
        """Receive a message from a client and send it so all other clients

        Args:
            client (object): client
        """
        while True:
            try:
                # Receive data from the socket. The return value is a bytes object
                # representing the data received. The maximum amount of data to be
                # received at once is specified by bufsize.
                mgs = client.recv(1024)
                self.broadcast(mgs)
            except Exception:
                # when a client leaves the server, a message is sent to all other clients
                index = self.clients.index(client)
                self.clients.remove(client)
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f"{nickname} left the chat!".encode("utf-8"))
                break

    def receive(self) -> None:
        """Create a tread for every client"""
        print("server is listening ...")
        while True:
            client, address = self.server.accept()
            print(f"connected with: {str(address)}")
            # if an new clients join the server, "NEW" will be sendet to the Client
            client.send("NEW".encode("utf-8"))
            # the answer is the nickname of the client
            nickname = client.recv(1024).decode("utf-8")
            self.nicknames.append(nickname)
            self.clients.append(client)
            print(f"Nickname of the client is {nickname}")
            # send to all clients
            self.broadcast(f"{nickname} joined the chat!".encode("utf-8"))
            # send only at client
            client.send("Your are connected!\nSend your Message here...".encode("utf-8"))
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


if __name__ == "__main__":
    server = CreateServer(auto_ip=True)
    server.receive()
