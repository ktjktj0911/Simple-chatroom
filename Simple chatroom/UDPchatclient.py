from socket import *
import threading

def receiver(clientSocket):
    while True:
        mMessage, serverAddress = clientSocket.recvfrom(2048)
        print(mMessage.decode())


serverName = input("server name: ")
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = '\0'
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
t1 = threading.Thread(target=receiver, args=(clientSocket,))
t1.start()
while True:
    message = input()
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    if message == "EXIT":
        break;
clientSocket.close()
