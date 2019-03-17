import socket
from threading import Thread


class Session(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket
        self.serverKill = False
        self.countDown = 0
        self.lines = []
        self.dateName = ""

    def run(self):
        while True:
            if self.serverKill:
                return
            try:
                msg = self.socket.recv(1024).decode("latin1")
                print("Message received: {}".format(msg))
                msg = msg.split("\n")
                print(msg)
                for message in msg:
                    self.__parse(message.split(" "))
            except UnicodeDecodeError:
                print("UNICODE DECODE ERROR")

    def __writetext(self):
        file = open("output/"+self.dateName+".txt", "w")
        for line in self.lines:
            file.write(line[0]+"\n")
        file.close()

    def __parse(self, msg):
        if msg == ['']:
            self.countDown += 1
            if self.countDown == 30:
                print("PROBLEM, closing connection")
                self.serverKill = True
                self.socket.close()
        else:
            self.countDown = 0
        if msg[0] == "SEND":
            print("Send signal")
            self.lines.append(msg[1:])
        elif msg[0] == "STOCK":
            print("Stock signal")
            self.__writetext()
            print("Wrote text tile: {}".format(self.dateName))
            self.lines.clear()
            self.dateName = ""
        elif msg[0] == "DESC":
            print("Desc signal")
            self.dateName = "".join(msg[1:])
        elif msg[0] == "END":
            print("End signal")
            self.socket.close()


def run():
    while True:
        print("Waiting connection from server.")
        socket, address = serverSocket.accept()
        c = Session(socket)
        sessions.append(c)
        c.start()


sessions = []
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 2049))  # 2049 is the port
serverSocket.listen(5)
run()
