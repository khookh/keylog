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
                msg = self.socket.recv(1024).recode("latin1")
                msg = msg[:-2].split(" ")
                self.parse(msg)
                print("Message received: {}".format(msg))
            except UnicodeDecodeError:
                print("UNICODE DECODE ERROR")

    def __writetext(self):
        file = open(self.dateName, "w")
        for line in self.lines:
            file.write(line)
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
        if msg[0] is "SEND":
            self.lines.append(msg[1:])
        elif msg[0] is "STOCK":
            self.__writetext()
            print("Wrote text tile: {}".format(self.dateName))
            self.lines.clear()
            self.dateName = ""
        elif msg[0] is "DESC":
            self.dateName = "".join(msg[1:])


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
