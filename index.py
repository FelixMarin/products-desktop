import sqlite3
from tkinter import *
from tkinter import ttk


class Product:

    db_name = 'database.db'

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

        #button add product
        ttk.Button(frame, text = 'Save product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        #Output message
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Table
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)
    
        #Buttons
        ttk.Button(text = 'DELETE', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        #filling products
        self.get_products()

    def run_query(self, query, parameters = ()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        result =cursor.execute(query, parameters)
        conn.commit()
        return result

    def get_products(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #query data
        query = 'SELECT * from product order by name desc' 
        db_rows = self.run_query(query)
        #filling data
        for row in db_rows:
            self.tree.insert('',0, text = row[1], values = row[2])
            
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query =  'INSERT INTO product VALUES(NULL,?,?)'
            parameters = (self.name.get(),self.price.get())
            self.run_query(query,parameters)
            self.message['text'] = 'Producto {} added Successfully'.format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            self.message['text'] = 'Name and Price are Required'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        val = self.tree.item(self.tree.selection())['text']
        if val == '':
            self.message['text'] = 'Please Select a Record'
            return 
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Record {} Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        val = self.tree.item(self.tree.selection())['text']
        if val == '':
            self.message['text'] = 'Please Select a Record'
            return       
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'

        #Old name
        Label(self.edit_wind, text = 'Old Name: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0 , column = 2)

        #new name 
        Label(self.edit_wind, text = 'New product').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        #Old price
        Label(self.edit_wind, text = 'Old price').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value= old_price), state = 'readonly').grid(row = 2, column = 2)
        
        #New price
        Label(self.edit_wind, text = 'New price').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda : self.edit_record(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W + E)

    def edit_record(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Product Edited'
        self.get_products()

if __name__ == '__main__':
  window = Tk()
  application = Product(window)
  window.mainloop()
