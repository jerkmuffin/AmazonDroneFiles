from OSC import OSCServer
from time import sleep

server = OSCServer( ("0.0.0.0", 8888) )
server.timeout = 0
run = True

def handle_timeout(self):
    self.timed_out = True

def cb(path, tags, args, source):
    if args[0] == 1:
        print("called back!")
    print(path, tags, args, source)


server.addMsgHandler("/yes/no", cb)

def each_frame():
    server.timed_out = False
    while not server.timed_out:
        server.handle_request()


while run:
    sleep(1)
    each_frame()

server.close()
