import base64
import json
import threading
import requests

destinationDevEUI = "70b3d54995bd3c5d"
class LNSSocket:
    def __init__(self, token):
        self.msgs = []
        self.msg_lock = threading.Lock()
        self.new_msg = threading.Condition(self.msg_lock)
        self.url = "https://core.acklio.net:8080/v1/devices/%s/send"
        self.token = token
        self.blocking = True
        self.timeout = None

    def from_lns(self, msg, address):
        with self.msg_lock:
            self.msgs.append((msg, address))
            self.new_msg.notify()

    
    def recvfrom(self, maxsize):
        print("Getting message waiting %s for it" % self.timeout)
        with self.msg_lock:
            while len(self.msgs) == 0:
                if self.blocking:
                    if not self.new_msg.wait(self.timeout):
                        raise TimeoutError("timed out waiting for message")
                else:
                    return None

            print("Got message")
            return self.msgs.pop()

    def setblocking(self, blocking):
        self.blocking = blocking

    def settimeout(self, timeout):
        self.timeout = timeout
        if self.timeout == 0:
            self.timeout = None

    def sendto(self, msg, address):
        
        answer = {
          "fport" : address["fPort"],
          "devEUI": address["devEUI"],
          "data"  : base64.b64encode(msg).decode('utf-8')
        }


        url = self.url % address["devEUI"] 
            
        cookieContent = {"access_token": self.token}
        print("**********Sending response %s, data=%s, cookies = %s" % (url, answer, cookieContent))
        print (requests.post(url, data=json.dumps(answer), cookies=cookieContent).text) 
