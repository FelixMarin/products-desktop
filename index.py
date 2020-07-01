from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    def __init__(self,window):
        self.wind = window
        self.wind.title('Products Application')

        #container
        frame = LabelFrame(self.wind, text = 'Register a new product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #name input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #price input
        Label(frame, text = 'Precio').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Table
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)

        #button add product
        ttk.Button(frame, text = 'Save product').grid(row = 3, columnspan = 2, sticky = W + E)

if __name__ == '__main__':
  window = Tk()
  application = Product(window)
  window.mainloop()