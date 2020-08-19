from socket import *
import threading

def receiver(clientSocket):
    while True:
        mMessage, serverAddress = clientSocket.recvfrom(1024)
        if mMessage.decode() == '\0':
            clientSocket.close()
            break
        print(mMessage.decode())

serverName = input("server name: ")
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
t1 = threading.Thread(target=receiver, args=(clientSocket,))
t1.start()
while True:
    message = input()
    clientSocket.send(message.encode())
    if message == "EXIT":
        break;
clientSocket.close()