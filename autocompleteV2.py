"""
    NOTES:


    url template for images ('http://gatherer.wizards.com/Handlers/Image.ashx?name=' + cardName + '&type=card&.jpg')
    url for edhrec.com ('https://edhrec.com/cards/' + cardName)
    url for edhrec avg deck ('https://edhrec.com/decks/' + cardName)

    url for http://store.tcgplayer.com/massentry

"""

from tkinter import *
import webbrowser
from urllib.request import *
# import io
import base64

root = Tk()
root.title("Ornithopter v0.1 Alpha")
root.resizable(width=False, height=False)

# set the canvas to card entered

'''
non working code to update the canvas

def get_card(card_entry):
    entry = card_entry.get()
    #image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=" + entry + "&type=card&.jpg"
    image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=Fall%20of%20the%20Hammer&type=card&.jpg"
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodebytes(image_byt)
    photo = tk.PhotoImage(data=image_b64)

    #global canvas = Canvas(bg='red')
    canvas.grid(row=2, column=0, rowspan=6, sticky=W+E+N+S, padx=5, pady=2)

    canvas.create_image(10, 10, image=photo, anchor='nw')
    print("function should be done")
'''

#Look up card in edhrec.com
def search_edh():
    card_entry = entry.get()
    webbrowser.open('https://edhrec.com/cards/' + card_entry)


def draw_canvas():
    card_entry = entry.get()
    #image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=" + entry + "&type=card&.jpg"
    print("function should be done")


def bind_test(self):
    try:
        print('enter was pressed')
        canvas.delete()
        image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=Yasova%20Dragonclaw&type=card&.jpg"
        image_byt = urlopen(image_url).read()
        print(str(image_url))
        image_b64 = base64.encodebytes(image_byt)
        photo = PhotoImage(data=image_byt)
        print('photo_test')
        print(str(photo))
        canvas.itemconfig(image_on_canvas, photo)
        print('function done')
    except TypeError:
        print('TypeError Occured')
        print(str(self.image_url))
        print(str(photo))
        print(str(image_on_canvas))
        print('end of error handling')
    else:
        print('No idea what happened')

test = Label(bg="red", text="Ornithopter v0.1 Alpha").grid(row=0, column=0, columnspan=3, sticky=W+E+N+S, padx=2, pady=2)

entry = StringVar()
card_entry = Entry(root, textvariable=entry)
card_entry.bind("<Return>", bind_test)
card_entry.grid()

# image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=" + test + "&type=card&.jpg"

image_url = "http://gatherer.wizards.com/Handlers/Image.ashx?name=Ornithopter&type=card&.jpg"

image_byt = urlopen(image_url).read()
image_b64 = base64.encodebytes(image_byt)
photo = PhotoImage(data=image_b64)


canvas = Canvas(bg='red')
canvas.grid(row=2, column=0, rowspan=7, sticky=W+E+N+S)
image_on_canvas = canvas.create_image(5, 5, image=photo, anchor=NW)

edh_button = Button(text='Search edhrec.com', command=search_edh)
edh_button.grid(row=2, column=1, sticky=W+E+N+S, padx=2, pady=2)

test1 = Button(text='Test')
test1.grid(row=3, column=1, sticky=W+E+N+S, padx=2, pady=2)

quit_button = Button(text="Quit", command=root.destroy)
quit_button.grid(row=5, column=2, sticky=W+E+N+S, padx=2, pady=2)


root.mainloop()
