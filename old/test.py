from tkinter import *
from PIL import Image
from urllib.request import *
import webbrowser
import base64
#----------------------------------------------------------------------

class MainWindow():

    #----------------

    def __init__(self, main):

        # canvas for image
        self.canvas = Canvas(main, width=600, height=400)
        self.canvas.grid(row=0, column=0)

        self.image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=Fall%20of%20the%20Hammer&type=card&.jpg"
        image_byt = urlopen(self.image_url).read()
        image_64 = base64.encodebytes(image_byt)
        self.photo = PhotoImage(data=image_64)
        
        self.image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=Ornithopter&type=card&.jpg"
        image_byt = urlopen(self.image_url).read()
        image_b64 = base64.encodebytes(image_byt)
        self.photo = PhotoImage(data=image_b64)

        # image_on_canvas = canvas.create_image(5, 5, image=photo, anchor=NW)




        img = Image.open("1.jpg")
        print(img.format)
        
        # images
        self.my_images = []
        self.my_images.append(PhotoImage(data=image_b64))
        self.my_images.append(PhotoImage(data=image_64))
        self.my_images.append(PhotoImage(file="3.jpg"))
        self.my_image_number = 0

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
        # button to change image
        self.button = Button(main, text="Change", command=self.onButton)
        self.button.grid(row=1, column=0)

    #----------------

    def onButton(self):

        # get url and set it with PhotoImage()
        self.image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=Ornithopter&type=card&.jpg"
        image_byt = urlopen(self.image_url).read()
        image_b64 = base64.encodebytes(image_byt)
        self.photo = PhotoImage(data=image_b64)

        # set canvas with photo
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)
#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
