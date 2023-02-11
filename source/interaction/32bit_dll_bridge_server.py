from socket import *
from time import ctime
import damo, threading
HOST = '127.0.0.1'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST,PORT)
 
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

dmdll = damo.DM()

def exec_rdata(rdata):
    func_name = rdata.split('$')[0]
    parameters = rdata.split('$')[1].split('#')[:-1]
    print(f"recieve: {func_name} {parameters}")
    if func_name == 'ver':
        return dmdll.ver()
    elif func_name == 'BindWindow':
        return dmdll.BindWindow(int(parameters[0]),str(parameters[1]),str(parameters[2]),str(parameters[3]),int(parameters[4]))
    elif func_name == 'EnableBind':
        return dmdll.EnableBind(int(parameters[0]))
    elif func_name == 'UnBindWindow':
        return dmdll.UnBindWindow()
    elif func_name == 'KeyDown':
        return dmdll.KeyDown(int(parameters[0]))
    elif func_name == 'KeyUp':
        return dmdll.KeyUp(int(parameters[0]))
    elif func_name == 'KeyPress':
        return dmdll.KeyPress(int(parameters[0]))
class server(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('...connnecting from:', addr)

            while True:
                data = tcpCliSock.recv(BUFSIZE)
                if not data:
                    break
                
                rdata = data.decode('utf-8')
                sdata = exec_rdata(rdata)
                
                tcpCliSock.send(sdata.encode())
                # tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
            tcpCliSock.close()
        tcpSerSock.close()

server().start()
import time
while 1:
    time.sleep(1)