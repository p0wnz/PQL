import socket
def connect(IP,port):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:client.connect((IP,port));return 0;   
    except:return 1;
def attempt_connect(ip,port,tries):
    i =1
    while i >=1 and i < tries:
        i = connect(ip,port)
        print i
        if i >=1:
            print "not connected"
            i+=1
        if i==0:
            break
            
    print "connected"
attempt_connect('127.0.0.1',810,35)
