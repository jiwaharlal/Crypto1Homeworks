#include <openssl/sha.h>
#include <string>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <iterator>
#include <vector>
#include <sstream>
#include <algorithm>
#include <memory>

using namespace std;

std::vector<unsigned char> sha256(const std::vector<char> aInput)
{
    unsigned char hash[SHA256_DIGEST_LENGTH];
    /*SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, aInput.data(), aInput.size());
    SHA256_Final(hash, &sha256);*/
    SHA256(reinterpret_cast<const unsigned char*>(aInput.data()), aInput.size(), hash);
    
    return std::vector<unsigned char>(hash, hash + SHA256_DIGEST_LENGTH);
}

std::string bytesToHexString(const std::vector<unsigned char>& aBytes)
{
    char buff[SHA256_DIGEST_LENGTH * 2];
    for (int i = 0; i < aBytes.size(); ++i) {
        sprintf(buff + i * 2, "%02x", aBytes[i]);
    }
    return string(buff);
}

int main(int argc, char* argv[])
{
    std::string fileName("example.mp4");
    if (argc == 2) {
        fileName = argv[1];
    }
    ifstream in(fileName, ifstream::in | ifstream::binary);
    if (!in.is_open()) {
        cerr << "Error opening file " << fileName << endl;
        return 0;
    }
    in.seekg(0, ifstream::end);
    int fileSize = in.tellg();
    int pos = fileSize / 1024 * 1024;
    int blockSize = fileSize - pos;
    
    
    std::vector<unsigned char> buffers[2];
    auto* readBuffer = buffers;
    auto* targetBuffer = buffers + 1;
    
    targetBuffer->resize(1024 + SHA256_DIGEST_LENGTH);
    readBuffer->resize(1024 + SHA256_DIGEST_LENGTH);
    in.seekg(pos);
    in.read(reinterpret_cast<char*>(readBuffer->data()), blockSize);
    
    SHA256(readBuffer->data(), blockSize, targetBuffer->data() + 1024);
    blockSize = 1024 + SHA256_DIGEST_LENGTH;
    
    while (pos != 0)
    {
        swap(readBuffer, targetBuffer);
        pos -= 1024;
        in.seekg(pos);
        in.read(reinterpret_cast<char*>(readBuffer->data()), 1024);
        SHA256(readBuffer->data(), blockSize, targetBuffer->data() + 1024);
    }
    
    cout << bytesToHexString(std::vector<unsigned char>(targetBuffer->data() + 1024, targetBuffer->data() + blockSize)) << endl;
    
    return 0;
    
    
    
    /*std::vector<char> readBuffer(blockSize, '\0');
    in.seekg(pos);
    in.read(readBuffer.data(), blockSize);
    auto shaCode = sha256(readBuffer);
    
    while (pos != 0)
    {
        readBuffer.resize(1024, '\0');
        pos -= 1024;
        in.seekg(pos);
        in.read(readBuffer.data(), 1024);
        std::copy(shaCode.begin(), shaCode.end(), back_inserter(readBuffer));
        shaCode = sha256(readBuffer);
    }
    
    cout << bytesToHexString(shaCode) << endl;
    
    return 0;*/
}
    