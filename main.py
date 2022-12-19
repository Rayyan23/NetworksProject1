from socket import *

serverPort = 7788
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
while True:
    connectionSocket, addr = serverSocket.accept()
    requestString = connectionSocket.recv(1024).decode()
    firstLine = requestString.split("\r\n")[0]
    print(firstLine)
    parts = firstLine.split(" ")
    if len(parts) != 0:
        if len(parts) == 3:
            file = parts[1]
            file = file.replace('/', '', 1)
            if file == "" or file == "index.html" or file == "main_en.html" or file == "en":
                file = "index.html"
            elif file == "ar":
                file = "indexAr.html"
            elif file == 'go' or file == "so" or file == "bzu":
                header = "HTTP/1.1 307 external Redirect\r\n"
                if file == "go":
                    header += "Location: https://www.google.com\r\n"
                elif file == "so":
                    header += "Location: https://stackoverflow.com\r\n"
                else:
                    header += "Location: https://www.birzeit.edu/\r\n"
                header += "Non-Authoritative-Reason: delegate"
                header = header.encode('utf-8')
                connectionSocket.send(header)
                connectionSocket.close()
                continue
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
                header = header.encode('utf-8')
                header += response
            except FileNotFoundError as e:
                header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\n'
                response = open('error404.html', 'rb').read()
                end = "<p>IP Address, Socket:" + str(addr[0]) + ", " + str(addr[1]) + "</p>\r\n</body>\r\n" \
                                                                                      "</html> "
                response += end.encode('utf-8')
                header = header.encode('utf-8')
                header += response
            connectionSocket.send(header)
            connectionSocket.close()
