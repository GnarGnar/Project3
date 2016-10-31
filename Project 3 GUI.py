from tkinter import *
from tkinter.ttk import *
from Crypto.Cipher import AES
ciphertext = ''
encryptedMessage=''
class Encryption():
  obj=AES.new('This is a key123',AES.MODE_CBC,'This is an IV456')
  message="The answer is no"
  global ciphertext
  ciphertext=obj.encrypt(message)
class Decryption():
  obj2=AES.new('This is a key123',AES.MODE_CBC,'This is an IV456')
  global ciphertext
  print(obj2.decrypt(ciphertext))

class App():
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()

    master.title("Project 3")
    self.label = Label(frame, text="Type very long text:")

    self.entry = Entry(frame)

    self.printEntry1 = Button(frame,text="Submit",width=15,command=self.printEntry)

    self.button = Button(frame,text="Quit", width=15,command=frame.quit)

    self.buttonCV= Button(frame,text="Turn on Camera",width=15,command=self.openCam)

    self.slogan = Button(frame,text="Hello", width=15,command=self.write_slogan)

    self.label.grid(row=0, column=0)
    self.entry.grid(row=0, column=1)
    self.slogan.grid(row=1, column=0,sticky='e')
    self.button.grid(row=3, column=1,sticky='e')
    self.buttonCV.grid(row=5,column=1,sticky='e')
    self.printEntry1.grid(row=2,column=1,sticky='e')

  def write_slogan(self):
    print ("Tkinter is easy to use!")
  def openCam(self):
    print("opens the camera")
  def printEntry(self):
    a=self.entry.get()
    print(a)

root = Tk()
root.style = Style()

#('clam', 'alt', 'default', 'classic')
root.style.theme_use("clam")
root.geometry("250x250")

app = App(root)
root.mainloop()