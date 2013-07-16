#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maxim
#
# Created:     11/07/2013
# Copyright:   (c) Maxim 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Crypto.Cipher import AES

def strToInts(str, len):
    result = []
    for i in range(0, len):
        result.append(int(str[i*2: i*2 + 2], 16))
    return result

def xorLists(lst1, lst2):
    result = []
    for i in range(0, len(lst1)):
        result.append(lst1[i] ^ lst2[i])
    return result

key1 = "140b41b22a29beb4061bda66b6747e14"
ciphertext1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

key2 = "140b41b22a29beb4061bda66b6747e14"
ciphertext2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

key3 = "36f18357be4dbd77f050515c73fcf9f2"
ciphertext3 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc3\
88d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"

key4 = "36f18357be4dbd77f050515c73fcf9f2"
ciphertext4 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa\
0e311bde9d4e01726d3184c34451"

def decode(key, ciphertext, mode):
    k = key.decode("hex")
    c = ciphertext.decode("hex")
    obj = AES.new(k, mode, c[0:16])
    return obj.decrypt(c[16:])

class CtrCounter:
    def __init__(self, initValue):
        self.value = initValue

    def __call__(self):
        v = self.value
        self.increaseValue()
        return v

    def increaseValue(self):
        i = ord(self.value[-1:])
        if i < 255:
            self.value = self.value[:-1] + chr(i + 1)
        else:
            j = self.value[-2:-1]
            self.value = self.value[:-2] + chr[j+1] + chr(0)


def decodeCtr(key, ciphertext):
    k = key.decode("hex")
    c = ciphertext.decode("hex")
    obj = AES.new(k, AES.MODE_CTR, counter = CtrCounter(c[0:16]))
    return obj.decrypt(c[16:])

def main():
    print decode(key1, ciphertext1, AES.MODE_CBC)
    print decode(key2, ciphertext2, AES.MODE_CBC)
    print decodeCtr(key3, ciphertext3)
    print decodeCtr(key4, ciphertext4)


if __name__ == '__main__':
    main()
