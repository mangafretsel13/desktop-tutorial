# importing socket module
from socket import *
import sys
import threading

def handle_request(connectionSocket):
    try:
        message = connectionSocket.recv(1024) #menerima request message dari client dengan buffer 1024 bytes
        filename = message.split()[1] #extract path object requested dari pesan, path merupakan bagian kedua dari http header, diidentifikai oleh [1]

        with open(filename[1:], 'rb') as f: #karena path yang di extrak dari http termasuk karakter '\', baca path dari karakter kedua
            outputdata = f.read() #baca file "f" dan simpan semua content dari requested file pada temporary buffer

        #mengirim https response header line pada koneksi soket
        connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n".encode())

        #mengirim konten yang diminta ke koneksi soket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])
        connectionSocket.send("\r\n".encode())
        connectionSocket.close() #tutup koneksi soket client

    except IOError: #mengirim http response kalo file ga ketemu
        #connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        with open('notfound.html', 'rb') as f: #karena path yang di extrak dari http termasuk karakter '\', baca path dari karakter kedua
            outputdata = f.read() #baca file "f" dan simpan semua content dari requested file pada temporary buffer

        #mengirim https response header line pada koneksi soket
        connectionSocket.send("HTTP/1.1 404 Not Found OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n".encode())

        #mengirim konten yang diminta ke koneksi soket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])
        connectionSocket.send("\r\n".encode())
        #connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()

#prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 7001
serverSocket.bind(('', serverPort)) #gabungin nomor port server dengan address
serverSocket.listen(5)  # Now the server can handle up to 5 requests simultaneously

running = True

while running:
    print('The server is ready to serve...')
    connectionSocket, addr = serverSocket.accept() #setting up new connection from the client
    thread = threading.Thread(target=handle_request, args=(connectionSocket,)) #membuat thread baru yg ngejalanin function handle_request dengan connection socket sebagai argumen
    thread.start()

serverSocket.close()
sys.exit()