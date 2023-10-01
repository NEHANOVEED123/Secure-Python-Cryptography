
P10 = ['3', '5', '2', '7', '4', '10', '1', '9', '8', '6']

P8 = ['6', '3', '7', '4', '8', '5', '10', '9']

P4 = ['2', '4', '3', '1']


IP = ['2', '6', '3', '1', '4', '8', '5', '7']

EP = ['4', '1', '2', '3', '2', '3', '4', '1']

S0 = \
[
        ['01', '00', '11', '10'],
        ['11', '10', '01', '00'],
        ['00', '10', '01', '11'],
        ['11', '01', '11', '10']
]

S1 = \
[
    ['00', '01', '10', '11'],
    ['10', '00', '01', '11'],
    ['11', '00', '01', '00'],
    ['10', '01', '00', '11']
]


IPInv = ['4', '1', '3', '5', '7', '2', '8', '6']

key1 = key2 = ""
class invalidKeyException(Exception):
    "exception raised when the input value is less than or greater than 10 bits"
    pass

def getKey():
    try:
        key = input("Enter 10-bit binary key.")
        i = 0
        if len(key) > 10 or len(key) < 10:
            raise invalidKeyException
        while i<len(key):
            if key[i] != '0' and key[i] != '1':
                key = input("Enter again 10-bit binary(0,1) key.")
                if len(key) > 10 or len(key) < 10:
                    raise invalidKeyException
                i = -1
            i =i + 1
        return key
    except invalidKeyException:
        print("exception occurred: invalid input of key")

def copy(src ,startIndex,endIndex):
    des = ""
    for i in range(startIndex,endIndex):
         des = des + src[i]
    return des

def initialPermutation(str):
    ipString= ""
    for i in IP:
        ipString = ipString + str[int(i) - 1]
    return ipString

def pTen(str):
    p_10String = ""
    for i in P10:
        p_10String = p_10String + str[int(i) - 1]
    return p_10String

def pEight(str):
    p_8String = ""
    for i in P8:
        p_8String = p_8String +str[int(i)-1]
    return p_8String

def leftShiftOne(str):
    temp = str[0]  # LS
    str = copy(str, 1, int(len(str)))
    str = str + temp
    return str

def leftShiftTwo(str):
    temp = str[0]+str[1]
    str = copy(str, 2, int(len(str)))
    str = str + temp
    return str

def keyGeneration():
    key = getKey()
    key = pTen(key)
    firstHalfKey = copy(key,0,int(len(key)/2))
    secondHalfKey = copy(key,5,len(key))
    firstHalfKey = leftShiftOne(firstHalfKey)
    secondHalfKey = leftShiftOne(secondHalfKey)
    global key1
    key1 = pEight(firstHalfKey+secondHalfKey)
    firstHalfKey = leftShiftTwo(firstHalfKey)
    secondHalfKey = leftShiftTwo(secondHalfKey)
    global key2
    key2 = pEight((firstHalfKey+secondHalfKey))

def cipherText():
    cipherText=input('Enter ciphertext: ')
    return cipherText
def expandPermutation(str):
    epString = ""
    for i in EP:
        epString = epString+str[int(i) -1]
    return epString
def p_4(str):
    p_4String = ""
    for i in P4:
        p_4String = p_4String+str[int(i) -1]
    return p_4String
def ipInverse(str):
    ipInverse = ""
    for i in IPInv:
       ipInverse = ipInverse+str[int(i) -1]
    return ipInverse
def XOR(str,key):
    result = ""
    i = 0
    while i < len(str):
        if str[i]==key[i]:
            result = result+'0'
        else:
            result= result+'1'
        i = i + 1
    return result
def sbox_0(str):
    row = int(str[0]+str[3],2)
    col = int(str[1]+str[2],2)
    return S0[row][col]
def sbox_1(str):
    row = int(str[0]+str[3],2)
    col = int(str[1]+str[2],2)
    return S1[row][col]
def round(str,key):
    leftHalf = copy(str, 0, int(len(str) / 2))
    rightHalf = copy(str, 4, int(len(str)))
    rightHalfAfterEP = expandPermutation(rightHalf)
    afterXorWithKey_1 = XOR(rightHalfAfterEP,key)
    leftHalf_afterXor = copy(afterXorWithKey_1, 0, int(len(afterXorWithKey_1) / 2))
    rightHalf_afterXor = copy(afterXorWithKey_1, 4, int(len(afterXorWithKey_1)))
    leftHalf_Sbox = sbox_0(leftHalf_afterXor)
    rightHalf_Sbox = sbox_1(rightHalf_afterXor)
    sboxStr = leftHalf_Sbox+rightHalf_Sbox
    afterP4 = p_4(sboxStr)
    return XOR(afterP4,leftHalf)

def decryption():
    print("     Decryption")
    text = cipherText()
    plainText = ""
    for char in text:
        asciiValue = ord(char)
        binary = format(asciiValue,'08b')
        afterIp = initialPermutation(binary)
        leftHalf = copy(afterIp,0,int(len(afterIp)/2))
        rightHalf = copy(afterIp,4,int(len(afterIp)))
        firstRoundResult = round(afterIp,key2)
        firstRoundResult = rightHalf + firstRoundResult
        rightHalf = copy(firstRoundResult, 4, int(len(firstRoundResult)))
        seconfRoundResult = round(firstRoundResult, key1)
        finalText = seconfRoundResult+rightHalf
        finalText = ipInverse(finalText)
        plainText = plainText + chr(int(finalText, 2))
    return plainText

def plainText():
    plainText=input('Enter Plain text: ')
    return plainText

def encryption():
    print("     Encryption")
    text = plainText()
    ciphetText = ""
    for char in text:
        asciiValue = ord(char)
        binary = format(asciiValue,'08b')
        afterIp = initialPermutation(binary)
        leftHalf = copy(afterIp,0,int(len(afterIp)/2))
        rightHalf = copy(afterIp,4,int(len(afterIp)))
        firstRoundResult = round(afterIp,key1)
        firstRoundResult = rightHalf + firstRoundResult
        rightHalf = copy(firstRoundResult, 4, int(len(firstRoundResult)))
        seconfRoundResult = round(firstRoundResult, key2)
        finalText = seconfRoundResult+rightHalf
        finalText = ipInverse(finalText)
        ciphetText = ciphetText + chr(int(finalText, 2))
    return ciphetText



keyGeneration()
print("Cipher Text:",encryption())
print("Plain Text:",decryption())
