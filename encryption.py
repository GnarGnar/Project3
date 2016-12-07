from Crypto.Cipher import AES
import os, binascii

rand_string2 = os.urandom(16)
rand_string = binascii.b2a_hex(os.urandom(16))

message =input('Please enter your message: ')
length = 16 - (len(message)%16)
x = len(message)
for x in range (length):
	message += " "
	
	
obj = AES.new(rand_string,AES.MODE_CBC,rand_string2)
ciphertext = obj.encrypt(message)
print("This is the encrypted message: ", ciphertext)
#print(rand_string)
#asciiKey = str(rand_string,'utf-8')
asciiKey = rand_string.decode()
print ("This is the message ",asciiKey)


obj2 = AES.new(asciiKey,AES.MODE_CBC,rand_string2)
plain_text = obj2.decrypt(ciphertext)
plain_text = plain_text.decode()
print(plain_text)
