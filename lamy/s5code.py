import socket
import time
import sys

class module():
    def _int_(self):
        return

    def s5comm(self):
        global HOST
        HOST = '192.168.1.3'
        global PORT1
        PORT1 = 2000
        global s1
        s1=socket.socket() 
        s1 = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s1.settimeout(30)
        s1.bind( (HOST, PORT1) )
        s1.listen(1)
        global c1, addr1
        c1, addr1 = s1.accept()
        print ("Communication Established to C3")
        return True

    def s5(self,msg):
        # print ("Message being sent to C3 is:  ",msg)

        try:
            # print ("Sending Message")
            msg=msg+"\r\n"
            c1.sendall(str.encode(msg))
            # print ("Command Sent to C3")
        except:
            print ("Sending Failed")
            sys.exit()

        # time.sleep(1)

        try:
            # print ("Awaiting Confirmation from C3")
            conf=""
            while conf== "":
                conf=c1.recv(1024)
            # print ("C3 sent a confirmation:  ",conf)
        except:
            print ("Receiving Failed")
            sys.exit()
        return

    def s5read(self):

        try:
            # print ("Reading from C3")
            conf=""
            while conf== "":
                conf=c1.recv(1024)
        except:
            print ("Receiving Failed")
            sys.exit()
        return conf