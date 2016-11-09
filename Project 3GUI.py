from tkinter import *
from tkinter.ttk import *
from Crypto.Cipher import AES
import numpy as np
import cv2
ciphertext=''

class App():
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
  
    master.title("Project 3")
    self.labelEncrypt = Label(frame, text="Encrypt")
    self.labelDecrypt= Label(frame,text="Decrypt")
    self.entryDecrypt=Entry(frame)
    self.entryEncrypt = Entry(frame)
    self.keyLabel = Label(frame,text="Key")
    self.keyEntry=Entry(frame)
    self.encryptEntry = Button(frame,text="Encrypt",width=15,command=self.encryptMessage)
    self.button = Button(frame,text="Quit", width=15,command=frame.quit)
    self.buttonCV= Button(frame,text="Turn on Camera",width=15,command=self.openCam)
    self.decryptEntry = Button(frame,text="Decrypt", width=15,command=self.decryptMessage)
    #entry boxes
    self.entryDecrypt.grid(row=2,column=1)
    self.keyEntry.grid(row=1,column=1)
    self.entryEncrypt.grid(row=0, column=1)
    #labels
    self.labelDecrypt.grid(row=2,column=0)
    self.labelEncrypt.grid(row=0, column=0)
    self.keyLabel.grid(row=1,column=0)
    self.decryptEntry.grid(row=3, column=1,sticky='e')
    self.button.grid(row=8, column=1,sticky='e')
    self.buttonCV.grid(row=8,column=0,sticky='e')
    self.encryptEntry.grid(row=3,column=0,sticky='e')
  
  def decryptMessage(self):
    message=self.entry.get()
    key1=self.entry2.get()
    obj2 = AES.new(key1,AES.MODE_CFB,'This is an IV456')
    global ciphertext
    decryptedMessage=obj2.decrypt(ciphertext)
    print("This is the decrypted message: ",decryptedMessage)

  def openCam(self):
    cap=cv2.VideoCapture(0)
    fist_cascade = cv2.CascadeClassifier('C:\\Users\\Ryan\\Desktop\\Project3-master\\fist.xml')
    while(True):
      ret,frame=cap.read()
      gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      fist=fist_cascade.detectMultiScale(gray,1.3,5)

      for(x,y,w,h) in fist:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,150,0),2)
      
      cv2.imshow('Fist',frame)
      if cv2.waitKey(1)&0xFF==ord('q'):
        break

    cap.release()

    cv2.destroyAllWindows()


  def encryptMessage(self):
    message=self.entry.get()
    key1=self.entry2.get()
    obj = AES.new(key1,AES.MODE_CFB,'This is an IV456')
    global ciphertext
    ciphertext=obj.encrypt(message)
    print("This is the encrypted message: ", ciphertext)

root = Tk()
root.style = Style()

#('clam', 'alt', 'default', 'classic')
root.style.theme_use("clam")
#root.geometry("500x500")

app = App(root)
root.mainloop()
