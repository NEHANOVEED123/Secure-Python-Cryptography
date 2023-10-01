
def key_generation(key):
    schedule = [i for i in range(0, 256)]
#256
    i = 0
    for j in range(0, 256):
        i = (i + schedule[j] + key[j % len(key)]) % 256

        temporary_var = schedule[j]
        schedule[j] = schedule[i]
        schedule[i] = temporary_var

    return schedule


def stream_generation_Function(schedule):
    stream = []
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (schedule[i] + j) % 256

        tempo = schedule[j]
        schedule[j] = schedule[i]
        schedule[i] = tempo

        yield schedule[(schedule[i] + schedule[j]) % 256]


def encrypt_data(text, key):
    text = [ord(char) for char in text]
    key = [ord(char) for char in key]

    schedule = key_generation(key)
    key_stream = stream_generation_Function(schedule)

    ciphertext = ''
    for char in text:
        encrypt = str(hex(char ^ next(key_stream))).upper()
        ciphertext += (encrypt)

    return ciphertext


def decrypt_data(ciphertext, key):
    ciphertext = ciphertext.split('0X')[1:]
    ciphertext = [int('0x' + c.lower(), 0) for c in ciphertext]
    key = [ord(char) for char in key]

    sched = key_generation(key)
    key_stream = stream_generation_Function(sched)

    plain_text = ''
    for char in ciphertext:
        decrypt = str(chr(char ^ next(key_stream)))
        plain_text += decrypt

    return plain_text




if __name__ == '__main__':
        key=input("Enter key : ")
        print("     Encryption")
        plain_text = input('Enter your plaintext: ')
        result = encrypt_data(plain_text, key)
        print('Cipher text is: ',result)
        #print(result)

        print("     Decryption")
        cipher_text = input('Enter your ciphertext: ')

        result = decrypt_data(cipher_text, key)
        print('Plain text is: ',result)

