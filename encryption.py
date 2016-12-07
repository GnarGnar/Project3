from Crypto.Cipher import AES
import os, binascii



def encryption():
	
	message =input('Please enter your message: ')
	length = 16 - (len(message)%16)
	x = len(message)
	for x in range (length):
		message += " "
	
	key = input('Please enter your key: ')
	keyLength = 16 - (len(key)%16)
	x = len(key)
	for x in range(keyLength):
		key += " "
	print(key)
	
	obj = AES.new(key,AES.MODE_CBC,'This is an IV456')
	ciphertext = obj.encrypt(message)
	print("This is the encrypted message: ", ciphertext)
	
	
	return ciphertext

def decryption(cipher):
	ciphertext = input('Please enter your message: ')
	
	key = input('Please enter your key: ')
	keyLength = 16 - (len(key)%16)
	x = len(key)
	for x in range(keyLength):
		key += " "
	print(key)
	obj2 = AES.new(key,AES.MODE_CBC,'This is an IV456')
	plain_text = obj2.decrypt(cipher)
	plain_text = plain_text.decode()
	print(plain_text)
	
	
cipher = encryption()

decryption(cipher);
