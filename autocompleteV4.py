"""
    NOTES:


    url template for images ('http://gatherer.wizards.com/Handlers/Image.ashx?name=' + cardName + '&type=card&.jpg')
    url for edhrec.com ('https://edhrec.com/cards/' + cardName)
    url for edhrec avg deck ('https://edhrec.com/decks/' + cardName)

    url for http://store.tcgplayer.com/massentry

    NOTE ON CANVAS BG:
    It might need some type of url encoding (HTTP 400 Bad Request gets returned if ramen in the set_canvas()
    has a space in it.  Also user agent might be incorrect but it's unlikely.  After successfully getting the url,
    need to find a way to set it properly with photoImage().  Then I can set the photoImage() variable into the canvas
    variable AND IT WILL ALL BE OVER!!!!!!!!

"""

from tkinter import *

# these 2 are for opening windows looking at the website
import webbrowser
import urllib
from urllib.request import *

# next 2 imports are for canvas
# import io

import base64
import json



root = Tk()
root.title("Ornithopter v0.1 Alpha")
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(1000, 1000))  # {w}x{h}

# set the canvas to card entered

# Open JSON File
with open('AllCards.json') as data_file:
    data = json.load(data_file)


# make a list from json file
lista = list(data.keys())


class UserAgent(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'



# Modified 3rd Party code for Autocomplete function
# Creates an autocomplete Entry GUI component
class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        
        # attributes
        completed_entry = StringVar()
        current_card = StringVar()
        card_type = StringVar()
        
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        
        # Ways user can autocomplete word
        self.bind("<Return>", self.selection)
        self.bind("<Right>", self.selection)
        self.bind("<Tab>", self.selection)
        
        # User toggles selection
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    # if user selected something, set the var and destroy lb
    def selection(self, event):

        if self.lb_up:
                        
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

            # set class attribute completed_entry to selected autocomplete word
            x = self.var.get()
            self.completed_entry = str.lower(x)  # lowercases everything to properly search

            # print(data['Air Elemental']['type'])
            # get the card type from selected name
            self.card_type = data[self.var.get()]['type']

            alert_label.config(text='Card is set')
            set_canvas(self.completed_entry)

    # move lb up by 1
    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    # move lb down by 1
    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    # compares the user entry input with a str list
    # python re is regular expression
    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')

        # need to modify this to only get the keys in json dictionary
        return [w for w in self.lista if re.match(pattern, w)]

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

# Look up card in edhrec.com


def set_canvas(ramen):
    # get url and set it with PhotoImage()
    
    '''
    # self.completed_entry
    image_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?name=' + ramen + '&type=card&.jpg'
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodebytes(image_byt)
    photo = PhotoImage(data=image_b64)
    '''
    
    # http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=368970&type=card
    
    url = 'http://gatherer.wizards.com/Handlers/Image.ashx?name=' + ramen + '&type=card&.jpg'

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                            '54.0.2840.71 Safari/537.36'
    
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()
    '''
    save = open('withHeaders.txt', 'w')
    save.write(str(resp_data))
    save.close()
    '''
    print(str(url))
    # response = urllib.request.urlopen(host)

    
    image_b64 = base64.encodebytes(resp_data)
    photo = PhotoImage(data=image_b64)
    
    save = open('test.txt', 'w')
    save.write(str(image_b64))
    save.close()
    #photo = PhotoImage(file="3.jpg")    

    # set canvas with photo
    canvas.itemconfig(image_on_canvas, image=photo)
    
    
def search_edh():
    webbrowser.open('https://edhrec.com/cards/' + entry.completed_entry)


def bind_test():
    '''
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
    '''
    print('enter was pressed')
    print(entry.completed_entry)


def search_avg_deck():
    # entry.completed_entry
    
    # Check if card has 'Legendary Creature in AutocompleteEntry.card_type
    if 'Legendary Creature' in entry.card_type:
        print('card is legendary creature')
        webbrowser.open('https://edhrec.com/decks/' + entry.completed_entry)
    else:
        alert_label.config(text='Card is not legendary type')
        print('card is not legendary creature')

left_side = Frame(root)
left_side.grid(row=0, column=0)

right_side = Frame(root)
right_side.grid(row=0, column=1)

test = Label(left_side, bg="red", text="Ornithopter v0.1 Alpha")
test.grid(row=0, column=0, columnspan=3, sticky=W+E+N+S, padx=2, pady=2)

entry = AutocompleteEntry(lista, left_side)
entry.grid(row=1, column=2)

edh_button = Button(left_side, text='Search edhrec.com', command=search_edh)
edh_button.grid(row=2, column=2, sticky=W+E+N+S, padx=2, pady=2)

avg_deck = Button(left_side, text='Get average deck', command=search_avg_deck)
avg_deck.grid(row=3, column=2, sticky=W+E+N+S, padx=2, pady=2)

test1 = Button(left_side, text='Test', command=bind_test)
test1.grid(row=4, column=2, sticky=W+E+N+S, padx=2, pady=2)

quit_button = Button(left_side, text="Quit", command=root.destroy)
quit_button.grid(row=5, column=2, sticky=W+E+N+S, padx=2, pady=2)

alert_label = Label(right_side, text="Card not set")
alert_label.grid(row=0, column=0, padx=2, pady=2)

photo = PhotoImage(file="4.jpg")

canvas = Canvas(right_side)
canvas.grid(row=1, column=0, rowspan=7, sticky=W+E+N+S)
image_on_canvas = canvas.create_image(5, 5, image=photo, anchor=NW)


root.mainloop()
