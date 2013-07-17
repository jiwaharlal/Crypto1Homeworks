#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maxim
#
# Created:     17/07/2013
# Copyright:   (c) Maxim 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib2
import requests
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
ciphertext = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------

def xorIntArrays(ar1, ar2):
    result = []
    for i in range(0, len(ar1)):
        result.append(ar1[i] ^ ar2[i])
    return result

def hexStringToIntArray(str):
    result = []
    for i in range(0, len(str) / 2):
        result.append(int(str[i*2: i*2 + 2], 16))
    return result

def intArrayToHexString(ar):
    result = ""
    for i in ar:
        result += "%02x" % i
    return result
    
def intArrayToNormalString(ar):
    result = ""
    for i in ar:
        result += chr(i)
    return result


class PaddingOracle(object):
    def __init__(self):
        self.initSymbolTable()
        self.blockLength = 16

    def initSymbolTable(self):
        self.symbolTable = [ord(' ')]
        self.symbolTable.append(9)
        for i in range(ord('a'), ord('z') + 1):
            self.symbolTable.append(i)
        for i in range(ord('A'), ord('Z') + 1):
            self.symbolTable.append(i)
        for i in range(1, 256):
            if not i in self.symbolTable:
                self.symbolTable.append(i)

    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        retry = True
        while retry:
            try:
                r = requests.get(target, timeout=1)
                retry = False
            except:
                print "timeout"
                pass
        # print "We got: {}".format(r.status_code)
        return (r.status_code == 404) | (r.status_code == 200)
        
        
        # req = urllib2.Request(target)         # Send HTTP request to server
        # try:
            # f = urllib2.urlopen(req)          # Wait for response
        # except urllib2.HTTPError, e:
            # print "We got: %d" % e.code       # Print response code
            # if e.code == 404:
                # return True # good padding
            # return False # bad padding

    def decrypt(self, ciphertext):
        self.ciphertext = ciphertext
        self.cipherBlocks = self.divideToBlocks(hexStringToIntArray(ciphertext))
        messageBlocks = []
        for i in range(0, len(self.cipherBlocks) - 1):
            messageBlocks.append(self.decryptBlock(i))
        message = ''
        for block in messageBlocks:
            message += intArrayToNormalString(block)
        return message

    def looksLikeFirstPaddingSymbol(self, messageBlock, symbolIndex):
        if symbolIndex == self.blockLength - 1:
            return False
        paddingValue = self.blockLength - symbolIndex
        for i in range(symbolIndex + 1, self.blockLength):
            if messageBlock[i] != paddingValue:
                return False
        return True
        
    def decryptBlock(self, blockIndex):
        msgHead = self.ciphertext[:(blockIndex) * 32]
        msgTail = self.ciphertext[(blockIndex + 1) * 32:(blockIndex + 2) * 32]

        messageBlock = []
        for i in range(0, 16):
            messageBlock.append(0)
        for symbolIndex in range(self.blockLength - 1, -1, -1):
            if self.looksLikeFirstPaddingSymbol(messageBlock, symbolIndex):
                messageBlock[symbolIndex] = messageBlock[symbolIndex + 1]
                continue
            paddingBlock = self.createPaddingFor(symbolIndex)
            for symbolCode in self.symbolTable:
                if symbolCode == (self.blockLength - symbolIndex):
                    continue
                messageBlock[symbolIndex] = symbolCode
                cipherBlock = xorIntArrays(xorIntArrays(self.cipherBlocks[blockIndex], messageBlock), paddingBlock)
                if self.query(msgHead + intArrayToHexString(cipherBlock) + msgTail):
                    print "Symbol found: ", chr(symbolCode)
                    break
            print "Message block: ", intArrayToHexString(messageBlock)    
        return messageBlock

    def createPaddingFor(self, incompleteBlockLength):
        result = []
        for i in range(0, incompleteBlockLength):
            result.append(0)
        paddingValue = self.blockLength - incompleteBlockLength
        for i in range(incompleteBlockLength, self.blockLength):
            result.append(paddingValue)
        return result

    def divideToBlocks(self, ar):
        result = []
        for i in range(0, len(ar)):
            if i % self.blockLength == 0:
                result.append([])
            result[len(result) - 1].append(ar[i])
        return result

if __name__ == "__main__":
    print "Ciphertext length: ", len(ciphertext)
    po = PaddingOracle()
    print po.createPaddingFor(10)
    print po.looksLikeFirstPaddingSymbol([3, 3, 3, 3, 3, 3, 3, 3, 9, 9, 9, 9, 9, 9, 9, 9], 7)
    blocks = po.divideToBlocks(hexStringToIntArray(ciphertext))
    print "Divided to {} blocks".format(len(blocks))
    print po.decrypt(ciphertext)
    #po.query(sys.argv[1])       # Issue HTTP query with the given argument