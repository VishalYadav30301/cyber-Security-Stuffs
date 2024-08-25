diction = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def userInterface():
    # read and write files
    fin = open('D:/Caesar Cipher/message.txt', 'r')
    fout = open('D:/Caesar Cipher/cipher.txt', 'w')
    container = fin.readlines()  # to store data in list form
    message = ''.join(container)  # to convert into string
    message = message.replace(" ", "")  # replacing blank with
    message = message.upper()  # converting all to uppercase letter
    userInput = input("Welcome to VishalTool \n Type 'e' for encryption =>  \n Type 'd' for decryption => ")

    if userInput == "e":
        print("Enter the key value => ")
        key = int(input())
        fout.write(Encrypt(message, key))
    elif userInput == "d":
        print("Enter the key value => ")
        key = int(input())
        fout.write(Decrypt(message, key))
    else:
        print("Entered choice is wrong ! ")
        userInterface()

    fin.close()
    fout.close()

location=0

def Encrypt(message, key):
    encrypted_message = ""
    for i in message:
        if i in diction:
            location = key + diction.index(i)
            location%=26
        encrypted_message += diction[location]
    print("Encryption is completed please check the Cipher.txt")
    return encrypted_message

location=0
def Decrypt(message, key):
    decrypted_message = ""
    for i in message:
        if i in diction:
            location = abs(key - diction.index(i))
            location%=26
        decrypted_message += diction[location]
    print("Decryption is completed please check the Cipher.txt")
    return decrypted_message

userInterface()
