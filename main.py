from socket import *

serverPort = 7788
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
while True:
    connectionSocket, addr = serverSocket.accept()
    requestString = connectionSocket.recv(1024).decode()
    firstLine = requestString.split("\r\n")[0]
    parts = firstLine.split(" ")
    if len(parts) != 0:
        if len(parts) == 3:
            file = parts[1]
            if file.startswith("/web"):
                file = "." + file
            if file == "/" or file == "/index.html" or file == "/main_en.html" or file == "/en":
                file = "./web/index.html"
            elif file == "/ar":
                file = "./web/indexAr.html"
            try:
                requestedFile = open(file, 'rb')
                response = requestedFile.read()
                requestedFile.close()
                header = 'HTTP/1.1 200 OK\n'
                if file.endswith(".JPG"):
                    mimetype = 'image/jpg'
                elif file.endswith(".png"):
                    mimetype = 'image/png'
                elif file.endswith(".css"):
                    mimetype = 'text/css'
                else:
                    mimetype = 'text/html'
                header += 'Content-Type: ' + str(mimetype) + '\n\n'
            except FileNotFoundError as e:
                header = 'HTTP/1.1 404 Not Found\n\n'
                response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP ' \
                           'Server</p></center></body></html>'.encode('utf-8')
            final_response = header.encode('utf-8')
            final_response += response
            connectionSocket.send(final_response)
