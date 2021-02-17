import socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('127.0.0.1',810))
sever.listen(5)
(client,address)=server.accept()
client.send("hello client")
