import tkinter as tk
from tkinter import ttk
from MyQR import myqr
from tkinter import filedialog
import os, binascii
import qrcode
import struct
import statistics
import imghdr
from Crypto.Cipher import AES
from PIL import ImageTk, Image
import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import base64
import os
import time


LARGE_FONT = ("Verdana", 12)
small_font = ("Verdana", 12)
hella_small_font = ("Verdana", 5)

class KinterEncrypter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)


        tk.Tk.wm_title(self, "Kinter Encrypter")
        container.pack(side = "top", fill  = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for f in (StartPage, MainPage):
            frame = f(container, self)

            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def combine_Funcs():
            controller.show_frame(MainPage)

        def openCam():
            global cap
            #opens the camera and imports a haar cascade for a fist for image recognition
            cap = cv2.VideoCapture(0)
            fist_cascade = cv2.CascadeClassifier('C:\\Users\\Ryan\\Desktop\\Project3\\fist.xml')
            while(True):
                ret, frame = cap.read()
                #converts the image to grayscale and searchs for the fist
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                fist = fist_cascade.detectMultiScale(gray,1.3,5)
                for(x,y,w,h) in fist:
                    #draws a rectangle around the 
                    cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
                    controller.show_frame(MainPage)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        label = ttk.Label(self, text = "Kinter Encrypter", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        button1 = ttk.Button(self, text = "Start", command = openCam)
        button1.pack()
        quitButton1 = ttk.Button(self,text="Quit", command = label.quit)
        quitButton1.place(x=15,y=300)



        # When everything done, release the capture



class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def encryptMessage():
            #message entry, makes sure message is a multiple of 16 bytes
            message = entryEncrypt.get()
            length = 16 - (len(message)%16)
            x = len(message)
            for x in range(length):
                message += " "
            #key entry, makes sure key is a multiple of 16 bytes
            key = keyEntry.get()
            keyLength = 16 - (len(key)%16)
            x = len(key)
            for x in range(keyLength):
                key += " "

            #encrypting message with the key entry...
            obj = AES.new(key,AES.MODE_CBC,'This is an IV456')
            cipherTextBytes = obj.encrypt(message)
            #converts the bytestring to a string
            cipherText = base64.b64encode(cipherTextBytes).decode('ascii')
            print("Key ..: ",key)
            print("Encrypted Message ...: ", cipherText)
            
                    
            
        def decryptMessage():
            cipherText = entryDecrypt.get()
            #converts the string to a bytestring
            cipherTextBytes = base64.b64decode(cipherText)
            key = keyEntry.get()
            keyLength = 16 - (len(key)%16)
            x = len(key)
            #makes sure key would be padded the same way as encryption
            for x in range(keyLength):
                key += " "
            #decrypting	
            obj2 = AES.new(key,AES.MODE_CBC,'This is an IV456')
            plain_text = obj2.decrypt(cipherTextBytes)
            #displays our plaintext
            plain_text = plain_text.decode()
            print("Decrypting the message ...: \n")
            time.sleep(5)
            print(plain_text)            



        tk.Frame.__init__(self, parent)
        #frame=Frame(master)
        #frame.pack()
        label = ttk.Label(self, text = " ", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        #####BUTTONS######
        encryptIt = ttk.Button(self,text = "Encrypt" , command = encryptMessage)
        decryptIt = ttk.Button(self,text="Decrypt", command = decryptMessage)
        hideImage = ttk.Button(self,text="Hide It", command =self.imageHider)
        quitButton = ttk.Button(self,text="Quit", command = label.quit)
        encryptIt.place(x = 15, y = 15)
        decryptIt.place(x=15,y=50)
        hideImage.place(x=15,y=100)
        quitButton.place(x=15,y=300)
        #####Entry######
        entryEncrypt = ttk.Entry(self,width=15)
        entryDecrypt = ttk.Entry(self,width=15)
        keyEntry = ttk.Entry(self,width=15)
        keyLabel = ttk.Label(self, text="Key.:", font=small_font)
        keyLabel.place(x=205,y=33)
        entryEncrypt.place(x = 100, y = 18)
        keyEntry.place(x=255,y=33)
        entryDecrypt.place(x=100,y=52)
        
    def imageHider(self):
        
      def LSB( pixVal, bit ):
          if bit == '1':
              pixVal = pixVal | 1 #00000001
          else:
              pixVal = pixVal & 254 #11111110
          return pixVal


      def getLSB( pixVal ):
          if pixVal & 1 == 0:
              return '0' 
          else:
              return '1'

      def hide(inFile, secretMess):
          secretMess = secretMess + chr(0) #It will be the end of secretMessage marker
          
          hiddenPixList = []
                  
          img = Image.open( inFile )
          img = img.convert('RGBA')  #four values per pixel
              
          pixList = list( img.getdata() )
              
          for i in range( len( secretMess ) ):
              asciiChar = ord( secretMess[i] )
              #print(asciiChar)
              binaryChar = bin( asciiChar ) [2:] .zfill( 8 )
              #print( binaryChar)    
              #Two separate lists keep the bits from alternating if they were stored in one list.
              hidePixEven = [] #contains bits 0-3
              hidePixOdd = []  #contains bits 4-7
                  
              pixEven = pixList[ i*2 ]    # two pixels per binary number
              pixOdd = pixList[ (i*2) +1 ]  
                  
              for k in range( 0, 4 ):
                  hidePixEven.append( LSB( pixEven[k], binaryChar[k] ) )
                  #print( hidePixEven)
                  hidePixOdd.append( LSB( pixOdd[k], binaryChar[ k+4 ] ) )    
                  #print(hidePixOdd)
              hpeTuple = tuple( hidePixEven )
              #print(hpeTuple)
              hpoTuple = tuple( hidePixOdd )
              #print(hpoTuple)  
              hiddenPixList.append( hpeTuple )
              hiddenPixList.append( hpoTuple )
              #print(hiddenPixList)
          unusedImgPart = pixList[ len(secretMess) *2: ]  #Splice n Dice the original image list
          hiddenPixList.extend( unusedImgPart )
          
          #for i in range(0,10):
              #print(hiddenPixList[i])
          
          newImg = Image.new( img.mode,img.size )
          newImg.putdata( hiddenPixList )
          newImg.save('hiddenImage.png')
          
          print("Success.")       


      def seek(hideFile):
          pixList=[]
          hiddenImg = Image.open(hideFile)
          hiddenImg = hiddenImg.convert('RGBA')
          pixList = list( hiddenImg.getdata() )
          #print(len(pixList))
          
          #for i in range( 100, 110):
          #print( pixList)
              
          messBinary ='0b'   
          decodeMess = ""
          bitCount = 0
          i=0
          
          while (messBinary != '0b00000000'):
              if bitCount == 8:
                  decodeMess += chr(int(messBinary,2))
                  messBinary = '0b'
                  bitCount = 0
              
              tupleVal = pixList[i]
              #print("tupleval")
              #print( tupleVal )
              for item in tupleVal:
                  #print("item")
                  #print( item )
                  messBinary += getLSB(item)
                  #print("getLSB")
                  #print( getLSB(item))
                  bitCount += 1
                  #print("bitcount")
                  #print(bitCount)
              i+= 1
              #print("i")
              #print( i)
              #wtf = input("pause")
          print("Your secret message: ")
          print( decodeMess )

      def hideImage( file1, file2):
          turkey = cv2.imread(file1)
          stuffing = cv2.imread(file2)
          width, height, channel = turkey.shape
          stuffing = cv2.resize(stuffing, (width,height) )
          bwStuff = cv2.cvtColor(stuffing, cv2.COLOR_BGR2GRAY)
          cv2.imshow('bw',bwStuff)
          
          
          
      #This is a check to see if the correct image is being processed.
      def seeBoth( inFile, hideFile ):
          imBefore = cv2.imread(inFile)
          imAfter = cv2.imread(hideFile)
          cv2.imshow('Before', imBefore)
          cv2.imshow('After', imAfter)
          cv2.waitKey(0)
          cv2.destroyAllWindows()
      
      #main
      #root = Tk()

      while( True ):
          print("Steganography")
          print("1. Encrypt Text")
          print("2. Decrypt Text")
          print("3. Compare before & after")
          print("4. Exit")
          choice = input("Enter your poison: ")
          if choice == '1':
              #http://stackoverflow.com/questions/11664443/raw-input-across-multiple-lines-in-python
              print("Enter your secret mess")
              #sentinel = 'team48'
              #secretMess = ''
              #for line in iter(input, sentinel): 
              secretMess=''+ '\n'.join(iter(input, 'team48' ))
              
              #secretMess = input("Enter you secret mess: ")
              print("Select your image: ")
              inFile = askopenfilename()
              print (inFile)
              #root.withdraw()
              hide( inFile, secretMess )
          elif choice == '2':
              print("Select your image: ")
              hideFile = askopenfilename()
              #root.withdraw()
              seek( hideFile )
          elif choice == '3':
              seeBoth( inFile, hideFile )
          elif choice == '4':
              print("Sbohem -czech")
              break
          elif choice =='5':
              file1 = 'Star-Wars-Darth-Vader-Wallpaper.png'
              file2= 'star-wars-yoda-spinoff-film.png'
              hideImage( file1, file2 )
          #inFile = 'Star-Wars-The-Force-Awakens-R2-D2.png'
          #hideFile = 'hiddenImage.png



app = KinterEncrypter()
path = "ig2.png"
photo = ImageTk.PhotoImage(file=path)
label2 = ttk.Label(app,image=photo)
label2.place(x=150,y=150)
app.geometry("350x350")
app.resizable(width=False,height=False)
app.mainloop()