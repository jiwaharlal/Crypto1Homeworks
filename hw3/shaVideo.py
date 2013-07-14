import sys
import os
from hashlib import sha256

def main():
    if len(sys.argv) != 2:
        fileName = "example.mp4"
    else:
        fileName = sys.argv[1]

    fileSize = os.stat(fileName).st_size
    pos = fileSize / 1024 * 1024
    blockSize = fileSize - pos

    f = open(fileName, 'rb')
    f.seek(pos)
    buff = f.read(blockSize)
    s = sha256(buff)
    print "File size: {}, pos: {}".format(fileSize, pos)
    try:
        while pos != 0:
            pos -= 1024
            f.seek(pos)
            buff = f.read(1024)
            s = sha256(buff + s.digest())
        print s.hexdigest()
    except:
        print "Error occured"
    finally:
        f.close()

main()
