
#comment this better and remove magic numbers

# going to regulate the string format
# We are making the signal format like "4 digits + signal + 0000"


class Comm:

    def __init__(self):
        return

    def readChunk(self,sock):
        chunk = ''
        lineLen = int(sock.recv(4))
        while lineLen > 0:
            chunk += sock.recv(lineLen)
            lineLen = int(sock.recv(4))
        return chunk

    def makeChunk(self,s):
        chunk = ''
        while len(s) > 9999:
            chunk += "9999" + s[:9999]
            s = s[9999:]
        lengthString = ''
        if len(s) < 10:
            lengthString = "000" + str(len(s))
        elif len(s) < 100:
            lengthString = "00" + str(len(s))
        else:
            lengthString = "0" + str(len(s))
        chunk += lengthString + s + "0000"
        return chunk
