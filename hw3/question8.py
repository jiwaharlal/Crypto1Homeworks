def ithInt(str, i):
    return int(str[i*2: i*2 + 2], 16)

def xorStrings(str1, str2):
    result = ""
    for i in range(0, len(str1)/2):
        x = ithInt(str1, i) ^ ithInt(str2, i)
        code = hex(x)[2:]
        if len(code) == 1:
            code = '0' + code
        result += code
    return result

def main():
    aes0 = "66e94bd4ef8a2c3b884cfa59ca342b2e"
    aes1 = "6f2584f0453f32f615c9afb7446b16f5"

    y2 = xorStrings(aes0, aes1)

    print "x1 = 0, y1 = 0"
    print "x2 = 1, y2 = ", y2
    print len(y2)

    print xorStrings("6666", "ffff")

main()
