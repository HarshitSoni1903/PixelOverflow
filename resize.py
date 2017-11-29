from tkinter import *

import tkFileDialog,tkMessageBox

from os.path import split,join,splitext,exists

class pixel:

    def toHex(self,i):

        hext = hex(i)
        hext = str(hext)
        hext = hext.split('x')[1]
        if(len(hext)%2!=0):
            hext='0'+hext
        return hext

    def getinfo(self,openfile):

        from PIL import Image
        im = Image.open(openfile)
        self.hext1 = self.toHex(im.size[1])
        self.hext2 = self.toHex(im.size[0])
        self.heightvar.set(im.size[1])
        self.widthvar.set(im.size[0])

    def change(self,savefile,newheight,newwidth):

        try:
            import binascii

            if('.' in self.pathvar.get()):
                extension = splitext(self.pathvar.get())[1]
                savefile = savefile + extension

            if(newwidth>65535):
                return False
            if(newheight>65535):
                return False
            if(newwidth<255):
                return False
            if(newheight<255):
                return False
            outhex1 = self.toHex(newheight)
            outhex2 = self.toHex(newwidth)

            if extension=='.png':
                outhex2=outhex2+'00'
                outhex1='00'+outhex1

                self.hext2=self.hext2+'00'
                self.hext1='00'+self.hext1
                self.hext = self.hext2 + self.hext1
                outhex = outhex2 + outhex1

            else:
                self.hext = self.hext1 + self.hext2
                outhex = outhex1+outhex2

            print outhex
            print self.hext

            with open(self.pathvar.get(), 'rb') as f:
                content = f.read()
            out = binascii.hexlify(content)



            base=split(self.pathvar.get())[0]

            savefile = join(base,savefile)

            if(exists(savefile)):
                return False

            out = out.replace(self.hext,outhex)

            output = open(savefile,'wb')

            content = binascii.unhexlify(out)
            output.write(content)
            output.close()

            return True
        except:
            return False

    def getpath(self):
        path = tkFileDialog.askopenfilename(title="Select File to Alter Pixels")
        self.pathvar.set(path)
        self.getinfo(path)


    def flood(self):

        if self.change(self.namevar.get(),self.heightvar.get(),self.widthvar.get()):
            tkMessageBox.showinfo(title="Success", message="The file has been filled with pixels according to the resolution entered.\nYou can find it in same folder as source file.")

        else:
            tkMessageBox.showerror(title="Please Try Again", message = "Some Error occurred, please try again.\n Common issues:\n 1. File is protected or corrupt. \n 2. File already Exists.\n3. Dimension of input as well as output must be in:\n\t256-65535.")

        self.pathvar.set("")
        self.widthvar.set("")
        self.heightvar.set("")
        self.namevar.set("")


    def gui(self,master):

        master.title("Pixel Burster")
        #master.iconbitmap(default='favicon.ico')
        master.geometry("520x100")
        master.resizable(False,False)
        self.Framei = Frame(master)
        self.Framei.pack()

        button1 = Button(self.Framei,text = "Browse", command = self.getpath)
        button2 = Button(self.Framei, text = "Begin", command = self.flood)
        label1 = Label(self.Framei, text = "File Path : ")
        label2 = Label(self.Framei, text = "New Height : ")
        label3 = Label(self.Framei, text = "New Width : ")
        label4 = Label(self.Framei, text = "New Name : ")

        self.pathvar = StringVar()
        self.pathvar.set("")
        self.namevar = StringVar()
        self.namevar.set("")
        self.heightvar = IntVar()
        self.heightvar.set("")
        self.widthvar = IntVar()
        self.widthvar.set("")

        entry1 = Entry(self.Framei, textvariable=self.pathvar, width=60)
        entry2 = Entry(self.Framei, textvariable=self.heightvar, width=17)
        entry3 = Entry(self.Framei, textvariable=self.widthvar, width=17)
        entry4 = Entry(self.Framei, textvariable=self.namevar, width=30)


        label1.grid(row=0,column=0,sticky=E)
        entry1.grid(row=0,column=1,columnspan=4,sticky=W)
        button1.grid(row=0,column=5,padx=(10,0))

        label2.grid(row=1, column=0,sticky=E)
        entry2.grid(row=1, column=1,sticky=W, columnspan=2)
        label3.grid(row=1, column=2, sticky=W)
        entry3.grid(row=1, column=3)

        label4.grid(row=3, column=0,sticky=E)
        entry4.grid(row=3, column=1,sticky=W)
        button2.grid(row=3, column=5,sticky=E, ipadx=5)


if __name__ == "__main__":
    root = Tk()
    ob = pixel()
    ob.gui(root)
    root.mainloop()