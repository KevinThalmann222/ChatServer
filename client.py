import socket
import threading


class Client:
    def __init__(self, auto_ip: bool = False, port: int = 9090) -> None:
        """Init

        Args:
            auto_ip (bool, optional): read the ip Automatic. Defaults to False.
            port (int, optional): ip Port. Defaults to 9090.
        """
        self.nickname = input("Choose your Nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if auto_ip:
            self.hostname = socket.gethostname()
        else:
            self.hostname = "10.3.164.44"

        self.client.connect((self.hostname, port))

    def receive(self) -> None:
        """Receive messages"""
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                # if the messae is "NEW" the nickname will be sendet to the server
                if message == "NEW":
                    self.client.send(self.nickname.encode("utf-8"))
                # else print the message in cmd
                else:
                    print(message)
            except Exception as ex:
                print(f"an error occurred: {ex}")
                self.client.close()
                break

    def write(self) -> None:
        """Send messages"""
        while True:
            message = f"{self.nickname}: {input('')}".encode("utf-8")
            self.client.send(message)

    def new_client(self) -> None:
        """Create a thread for a client"""
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()
        

if __name__ == "__main__":
    client = Client(auto_ip=True)
    client.new_client()
