"""
    NOTES:
    If going to work again, start from v4

    url template for images ('http://gatherer.wizards.com/Handlers/Image.ashx?name=' + cardName + '&type=card&.jpg')
    url for edhrec.com ('https://edhrec.com/cards/' + cardName)
    url for edhrec avg deck ('https://edhrec.com/decks/' + cardName)

    url for http://store.tcgplayer.com/massentry

"""

from tkinter import *
import webbrowser
import json
import unicodedata

# Modified 3rd Party code for Autocomplete function
# Creates an autocomplete Entry GUI component

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)

        # attributes
        completed_entry = StringVar()
        current_card = StringVar()
        name_set = StringVar()
        card_type = StringVar()
        mana_set = StringVar()
        cmc_set = StringVar()
        text_set = StringVar()

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

            # get the card info and set it to the labels in the tkinter gui
            self.name_set = data[self.var.get()]['name']
            name.config(text=self.name_set)

            self.mana_set = data[self.var.get()]['manaCost']
            mana.config(text=self.mana_set)

            self.cmc_set = data[self.var.get()]['cmc']
            cmc.config(text=self.cmc_set)

            self.card_type = data[self.var.get()]['type']
            type_card.config(text=self.card_type)

            self.text_set = data[self.var.get()]['text']
            text.config(text=self.text_set )
            
            # set output label
            alert_label.config(text="Card has been set")
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


# Look up card in edhrec.com
def search_edh():
    webbrowser.open('https://edhrec.com/cards/' + entry.completed_entry)


def search_avg_deck():
    # entry.completed_entry

    # Check if card has 'Legendary Creature in AutocompleteEntry.card_type
    if 'Legendary Creature' in entry.card_type:
        print('card is legendary creature')
        webbrowser.open('https://edhrec.com/decks/' + entry.completed_entry)
    else:
        alert_label.config(text='Card is not legendary type')
        print('card is not legendary creature')

root = Tk()
root.title("Ornithopter v0.1 Alpha")
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(450, 400))  # {w}x{h}


# Open JSON File
with open('AllCards.json') as data_file:
    data = json.load(data_file)

# make a list from json file
lista = list(data.keys())

main_frame = Frame(root)
main_frame.grid()
# main_frame.pack(fill="both", expand=True, padx=20, pady=20)

left_side = Frame(main_frame)
left_side.grid(row=0, column=0, padx=2, pady=2)
# left_side.pack()
# left_side.pack(fill="both", expand=True, padx=20, pady=20)

alert_label = Label(left_side, text="Card not set")
alert_label.grid(row=0, column=0, padx=2, pady=2)

entry = AutocompleteEntry(lista, left_side)
entry.grid(row=1, column=0)

edh_button = Button(left_side, text='Search edhrec.com', command=search_edh)
edh_button.grid(row=2, column=0, sticky=W + E + N + S, padx=2, pady=2)

avg_deck = Button(left_side, text='Get average deck', command=search_avg_deck)
avg_deck.grid(row=3, column=0, sticky=W + E + N + S, padx=2, pady=2)

quit_button = Button(left_side, text="Quit", command=root.destroy)
quit_button.grid(row=5, column=0, sticky=W + E + N + S, padx=2, pady=2)


middle_frame = Frame(main_frame)
middle_frame.grid(row=0, column=1, padx=2, pady=2)
# middle_frame.pack()
# middle_frame.pack(fill="both", expand=True, padx=20, pady=20)

'''
right_side = Frame(main)
# right_side.grid(row=0, column=2)
right_side.pack()
'''


'''
      "name":"Air Elemental",
      "manaCost":"{3}{U}{U}",
      "cmc":5,
      "colors":[
         "Blue"
      ],
      "type":"Creature — Elemental",
      "types":[
         "Creature"
      ],
      "subtypes":[
         "Elemental"
      ],
      "text":"Flying",
      "power":"4",
      "toughness":"4",
      "imageName":"air elemental",
      "colorIdentity":[
         "U"

'''

name_frame = Frame(middle_frame)
# name_frame.pack()
name_frame.grid(row=0, column=0)

name_label = Label(name_frame, text="Card Name:  ")
# name_label.pack(side=LEFT)
name_label.grid(row=0, column=0)

name = Label(name_frame, wraplength=200, text="")
# name.pack(side=RIGHT)
name.grid(row=0, column=1)

mana_frame = Frame(middle_frame)
# mana_frame.pack()
mana_frame.grid(row=1, column=0)

mana_label = Label(mana_frame, text="Mana Cost:  ")
# mana_label.pack(side=LEFT)
mana_label.grid(row=0, column=0)

mana = Label(mana_frame, wraplength=200, text="")
# mana.pack(side=RIGHT)
mana.grid(row=0, column=1)

cmc_frame = Frame(middle_frame)
# cmc_frame.pack()
cmc_frame.grid(row=2, column=0)

cmc_label = Label(cmc_frame, text="CMC:  ")
# cmc_label.pack(side=LEFT)
cmc_label.grid(row=0, column=0)

cmc = Label(cmc_frame, wraplength=200, text="")
# cmc.pack(side=RIGHT)
cmc.grid(row=0, column=1)

type_frame = Frame(middle_frame)
# type_frame.pack()
type_frame.grid(row=3, column=0)

type_label = Label(type_frame, text="Card Type:  ")
# type_label.pack(side=LEFT)
type_label.grid(row=0, column=0)

type_card = Label(type_frame, wraplength=200, text="")
# type_card.pack(side=RIGHT)
type_card.grid(row=0, column=1)

text_frame = Frame(middle_frame)
# text_frame.pack()
text_frame.grid(row=4, column=0)

text_label = Label(text_frame, text="Card Text:  ")
# text_label.pack(side=LEFT)
text_label.grid(row=0, column=0)

text = Label(text_frame, wraplength=200, text="")
# text.pack(side=RIGHT)
text.grid(row=1, rowspan=4, columnspan=1)

root.mainloop()
