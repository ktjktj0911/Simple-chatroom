from socket import *
import threading
numCount = 0

def chat(serverSocket, connectionSocket, clientAddress, Addr, x, N):
    global numCount
    while numCount >= N:
        print("<" + str(clientAddress[0]) + ", " + str(clientAddress[1]) + "> was blocked")
        connectionSocket.sendto('\0'.encode(), clientAddress)
        connectionSocket.close()
        connectionSocket, clientAddress = serverSocket.accept()
    numCount = numCount + 1
    greet = "<" + str(clientAddress[0]) + ", " + str(clientAddress[1]) + "> has entered a chatroom..."
    print(greet)
    connectionSocket.sendto("Welcome to ELEC4120 chatroom!".encode(), clientAddress)
    Addr[x][0] = connectionSocket
    Addr[x][1] = clientAddress
    for i in range(2*N):
        if i != x and Addr[i][0] != '0':
            Addr[i][0].sendto(greet.encode(), Addr[i][1])
    while True:
        message = connectionSocket.recv(1024)
        if message.decode() == "EXIT":
            exit = "<" + str(Addr[x][1][0]) + ", " + str(Addr[x][1][1]) + "> has left a chatroom..."
            print(exit)
            for i in range(2*N):
                if i != x and Addr[i][0] != '0':
                    Addr[i][0].sendto(exit.encode(), Addr[i][1])
            Addr[x][0].close()
            Addr[x][0] = '0'
            Addr[x][1] = '0'
            numCount = numCount - 1
            connectionSocket, clientAddress = serverSocket.accept()
            while numCount >= N:
                print("<" + str(clientAddress[0]) + ", " + str(clientAddress[1]) + "> was blocked")
                connectionSocket.sendto('\0'.encode(), clientAddress)
                connectionSocket.close()
                connectionSocket, clientAddress = serverSocket.accept()
            numCount = numCount + 1
            greet = "<" + str(clientAddress[0]) + ", " + str(clientAddress[1]) + "> has entered a chatroom..."
            print(greet)
            connectionSocket.sendto("Welcome to ELEC4120 chatroom!".encode(), clientAddress)
            Addr[x][0] = connectionSocket
            Addr[x][1] = clientAddress
            for i in range(2*N):
                if i != x and Addr[i][0] != '0':
                    Addr[i][0].sendto(greet.encode(), Addr[i][1])
            continue
        modifiedMessage = "<" + str(clientAddress[0]) + ", " + str(clientAddress[1]) + "> " + message.decode()
        print(modifiedMessage)
        connectionSocket.send("<You> ".encode() + message)
        for j in range(2*N):
            if j != x and Addr[j][0] != '0':
                Addr[j][0].sendto(modifiedMessage.encode(), Addr[j][1])
    connectionSocket.close()
    serverSocket.close()


N = int(input("Type number of clients to support: "))
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(N)
print('Server ready')
Addr = [[0 for x in range(2)] for y in range(2*N)]
for i in range(2*N):
    Addr[i][0] = '0'
    Addr[i][1] = '0'
T = [0 for x in range(2*N)]
x = 0
for x in range(2*N):
    connectionSocket, clientAddress = serverSocket.accept()
    T[x] = threading.Thread(target=chat, args=(serverSocket, connectionSocket, clientAddress, Addr, x, N,))
    T[x].start()