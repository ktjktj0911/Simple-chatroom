from socket import *
N = int(input("Type number of clients to support: "))
Addr = [0 for x in range(N)]
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("Server Ready")
x = 0
while x <= N:
    message, clientAddress = serverSocket.recvfrom(2048)
    if message.decode() == '\0':
        if x == N:
            print("<" + str(clientAddress[0]) + "," + str(clientAddress[1]) + "> was blocked")
            continue
        Addr[x] = clientAddress
        greet = "<" + str(clientAddress[0]) + "," + str(clientAddress[1]) + "> has entered a chatroom..."
        print(greet)
        serverSocket.sendto("Welcome to ELEC4120 chatroom!".encode(), clientAddress)
        z = 0
        while z < x:
            serverSocket.sendto(greet.encode(), Addr[z])
            z = z + 1
        x = x + 1
        continue
    if message.decode() == "EXIT":
        exit = "<" + str(clientAddress[0]) + "," + str(clientAddress[1]) + "> has left the chatroom"
        print(exit)
        z = 0
        while z < x:
            if clientAddress == Addr[z]:
                break
            z = z + 1
        for i in range(z, x-1):
            if z+1 == x:
                Addr[z+1] = 0
            Addr[i] = Addr[i+1]
        x = x - 1
        for z in range(x):
            serverSocket.sendto(exit.encode(), Addr[z])
        continue
    modifiedMessage = "<" + str(clientAddress[0]) + "," + str(clientAddress[1]) + "> " + message.decode()
    print(modifiedMessage)
    serverSocket.sendto("<You> ".encode() + message, clientAddress)
    y = 0
    while y < x:
        if clientAddress != Addr[y]:
            serverSocket.sendto(modifiedMessage.encode(), Addr[y])
        y = y + 1

