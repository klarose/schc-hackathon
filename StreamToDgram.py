class StreamToDgram:
  def __init__(self, sock):
    self.sock = sock

  def sendto(self, msg, address):
    return self.sock.send(msg)

  def recvfrom(self, max_size):
    return (self.sock.recv(max_size), None)
