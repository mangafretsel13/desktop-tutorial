from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 7001
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('The server is ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
  
        f = open(filename[1:])
        outputdata = f.read()
  
        connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n".encode()) #sends a 200 OK header line

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode()) 
        connectionSocket.close()
  
    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
  
        connectionSocket.close() 
serverSocket.close()
sys.exit()