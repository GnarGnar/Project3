
from PIL import Image


from tkinter import Tk
from tkinter.filedialog import askopenfilename




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
    newImg.show()
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

  
#main
root = Tk()
while( True ):
    
    
    print("Steganography - Text")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    choice = input("Enter your poison: ")
    if choice == '1':
        secretMess = input("Enter you secret mess: ")
        print("Select your image: ")
        
       
        inFile = askopenfilename()
        print (inFile)
        root.withdraw()
        
        
        hide( inFile, secretMess )
    elif choice == '2':
        print("Select your image: ")

        hideFile = askopenfilename()
        #root.withdraw()
        
        seek( hideFile )
    elif choice == '3':
        print("Proshchay")
        break
    
    
    #inFile = 'Star-Wars-The-Force-Awakens-R2-D2.png'
    #hideFile = 'hiddenImage.png'
     
    


    
    

