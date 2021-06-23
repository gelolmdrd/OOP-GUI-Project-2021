from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

root = Tk()
root.title("Final Project | GROUP 8")
root.iconbitmap('icon.ico')
root.minsize(1080, 690)
root.maxsize(1080, 690)
root.geometry("1080x690")
root.configure(bg='white')

# Create a database or connect to one
conn = sqlite3.connect('shoes_inventory.db')

# Create cursor
c = conn.cursor()

# Create a table if table does not exist yet
c.execute(""" CREATE TABLE if not exists inventory (
    shoe_sku text,
    shoe_name text,
    shoe_type text,
    shoe_color text,
    shoe_brand text,
    shoe_gender text,
    shoe_size real,
    shoe_price real)
    """)

# Commit Changes
conn.commit()

# Close Connection
conn.close()

# Simple function to make uppercase letters


def caps(event):
    sku.set(sku.get().upper())
    search_sku.set(search_sku.get().upper())

# Create a Query function for database


def query_database():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('shoes_inventory.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT * FROM inventory")
    records = c.fetchall()

    # Add our data to the screen
    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            results.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]), tags=('evenrow'))

        else:
            results.insert(parent='', index='end',  iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]), tags=('oddrow'))
        # increment counter
        count += 1

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

# Create Submit Function for database


def submit():
    if shoe_sku.get() and shoe_name.get() and shoe_type.get() or shoe_color.get() and shoe_brand.get() and shoe_gender.set('') and shoe_size.get() and shoe_price.get() != '':
        if len(shoe_sku.get()) == 12:
            # Create a database or connect to one
            conn = sqlite3.connect('shoes_inventory.db')

            # Create cursor
            c = conn.cursor()

            c.execute("SELECT * FROM inventory WHERE shoe_sku = :shoe_sku",
                      {
                          'shoe_sku': shoe_sku.get(),

                      })
            entry = c.fetchone()

            if entry is None:
                # Insert Into Table
                c.execute("""INSERT INTO inventory 
                        VALUES (:shoe_sku, :shoe_name, :shoe_type, :shoe_color, :shoe_brand, :shoe_gender, :shoe_size, :shoe_price)""",
                          {
                              'shoe_sku': shoe_sku.get(),
                              'shoe_name': shoe_name.get(),
                              'shoe_type': shoe_type.get(),
                              'shoe_color': shoe_color.get(),
                              'shoe_brand': shoe_brand.get(),
                              'shoe_gender': shoe_gender.get(),
                              'shoe_size': shoe_size.get(),
                              'shoe_price': shoe_price.get(),
                          })

                # Commit Changes
                conn.commit()

                # Close Connection
                conn.close()

                shoe_sku.delete(0, END)
                shoe_name.delete(0, END)
                shoe_type.set('')
                shoe_color.set('')
                shoe_brand.delete(0, END)
                shoe_gender.set('')
                shoe_size.set('')
                shoe_price.delete(0, END)

            else:
                messagebox.showerror(
                    "Error", "Record with the same SKU already exists")

        else:
            messagebox.showwarning(
                "Warning!", "SKU must contain 12 alphanumeric characters")

    else:
        messagebox.showwarning("Warning!", "Entry boxes must contain data!")

    # Clear The Treeview Table
    results.delete(*results.get_children())

    # Run to pull data from database on start
    query_database()


# Create an Update function


def update():
    if shoe_sku.get() or shoe_name.get() or shoe_type.get() or shoe_color.get() or shoe_brand.get() or shoe_gender.set('') or shoe_size.get() or shoe_price.get() != '':
        # Grab the record number
        selected = results.focus()
        # Update record
        results.item(selected, values=(shoe_sku.get(), shoe_name.get(), shoe_type.get(
        ), shoe_color.get(), shoe_brand.get(), shoe_color.get(), shoe_size.get(), shoe_price.get(),))

        # Update the database
        # Create a database or connect to one that exists
        conn = sqlite3.connect('shoes_inventory.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute("""UPDATE inventory SET 
        shoe_sku = :shoe_sku, 
        shoe_name = :shoe_name,
        shoe_type = :shoe_type,
        shoe_color = :shoe_color, 
        shoe_brand = :shoe_brand,
        shoe_gender = :shoe_gender, 
        shoe_size = :shoe_size, 
        shoe_price = :shoe_price

            WHERE shoe_sku = :shoe_sku""",
                  {
                      'shoe_sku': shoe_sku.get(),
                      'shoe_name': shoe_name.get(),
                      'shoe_type': shoe_type.get(),
                      'shoe_color': shoe_color.get(),
                      'shoe_brand': shoe_brand.get(),
                      'shoe_gender': shoe_gender.get(),
                      'shoe_size': shoe_size.get(),
                      'shoe_price': shoe_price.get(),

                  })

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear The Text Boxes
        shoe_sku.delete(0, END)
        shoe_name.delete(0, END)
        shoe_type.set('')
        shoe_color.set('')
        shoe_brand.delete(0, END)
        shoe_gender.set('')
        shoe_size.set('')
        shoe_price.delete(0, END)

        # Clear The Treeview Table
        results.delete(*results.get_children())

        # Run to pull data from database on start
        query_database()

    else:
        messagebox.showwarning("Warning!", "Select a record to Update!")

# Create a Show function to show results


def show():
    # Clear The Treeview Table
    results.delete(*results.get_children())

    # Run to pull data from database on start
    query_database()

# Create a Search function to search for a record


def search():
    if shoe_search.get() != '':
        # Create a database or connect to one
        conn = sqlite3.connect('shoes_inventory.db')

        # Create cursor
        c = conn.cursor()

        c.execute("SELECT * FROM inventory WHERE shoe_sku = :shoe_sku",
                  {
                      'shoe_sku': shoe_search.get(),

                  })
        entry = c.fetchone()

        if entry is None:
            messagebox.showerror(
                "Error", "Item with the indicated SKU not found!")

            # Clear The Treeview Table
            results.delete(*results.get_children())

            # Run to pull data from database on start
            query_database()

        else:
            # Clear The Treeview Table
            results.delete(*results.get_children())

            results.insert(parent='', index='end', iid=count, text='',
                           values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7]), tags=('evenrow'))

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
    else:
        messagebox.showwarning("Warning!", "Search box must contain the SKU!")

    shoe_search.delete(0, END)

# Create Delete fucntion to delete A record


def delete():
    if shoe_sku.get() or shoe_name.get() or shoe_type.get() or shoe_color.get() or shoe_brand.get() or shoe_gender.set('') or shoe_size.get() or shoe_price.get() != '':
        response = messagebox.askyesno(
            "Confirm?", "Do you want to delete this record?")
        if response == 1:

            x = results.selection()[0]

            conn = sqlite3.connect('shoes_inventory.db')

            # Create cursor
            c = conn.cursor()

            # Delete a record
            c.execute("""DELETE from inventory 
                        WHERE shoe_sku = :shoe_sku""",
                      {
                          'shoe_sku': shoe_sku.get(),
                      })

            # Commit Changes
            conn.commit()

            # Close Connection
            conn.close()

            # Clear The Text Boxes
            shoe_sku.delete(0, END)
            shoe_name.delete(0, END)
            shoe_type.set('')
            shoe_color.set('')
            shoe_brand.delete(0, END)
            shoe_gender.set('')
            shoe_size.set('')
            shoe_price.delete(0, END)

            # Clear The Treeview Table
            results.delete(*results.get_children())

            # Run to pull data from database on start
            query_database()

        else:
            pass

    else:
        messagebox.showerror("Error", "Please select a record to delete!")

# Create a Delete All function


def del_all():
    response = messagebox.askyesno(
        "Confirm?", "Do you want to delete ALL your record?")
    if response == 1:
        # Create a database or connect to one
        conn = sqlite3.connect('shoes_inventory.db')
        # Create cursor
        c = conn.cursor()

        # Delete a record
        c.execute("DELETE from inventory ")

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()

        # Clear The Treeview Table
        results.delete(*results.get_children())

        # Run to pull data from database on start
        query_database()

    else:
        pass

# Create a Select function to select results from Treeview


def select():
    # Clear The Text Boxes
    shoe_sku.delete(0, END)
    shoe_name.delete(0, END)
    shoe_type.set('')
    shoe_color.set('')
    shoe_brand.delete(0, END)
    shoe_gender.set('')
    shoe_size.set('')
    shoe_price.delete(0, END)

    # Grab record Number
    selected = results.focus()
    # Grab record values
    values = results.item(selected, 'values')

    # outputs to entry boxes
    shoe_sku.insert(0, values[0])
    shoe_name.insert(0, values[1])
    shoe_type.set(values[2])
    shoe_color.set(values[3])
    shoe_brand.insert(0, values[4])
    shoe_gender.set(values[5])
    shoe_size.set(values[6])
    shoe_price.insert(0, values[7])


def clear():
    if shoe_sku.get() or shoe_name.get() or shoe_type.get() or shoe_color.get() or shoe_brand.get() or shoe_gender.set('') or shoe_size.get() or shoe_price.get() != '':
        # Clear The Text Boxes
        shoe_sku.delete(0, END)
        shoe_name.delete(0, END)
        shoe_type.set('')
        shoe_color.set('')
        shoe_brand.delete(0, END)
        shoe_gender.set('')
        shoe_size.set('')
        shoe_price.delete(0, END)
    else:
        messagebox.showerror("Error", "Entry boxes already empty!")


# Frames
top_divider = Frame(root, height=20, width=2080, bg='red4')
top_divider.place(relx=0, rely=0.11)

bottom_divider = Frame(root, height=15, width=2080, bg='red4')
bottom_divider.place(relx=0, rely=0.4)

search_frame = Frame(root, height=120, width=300, bg='coral1')
search_frame.place(relx=0.65, rely=0.16)

results_frame = Frame(root, height=370, width=1035, bg='coral1')
results_frame.place(relx=0.5, rely=0.705, anchor="center")

# Add Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
                background="red4",
                foreground="black",
                rowheight=20,
                fieldbackground="white")

# Change Selected Color
style.map('Treeview',
          background=[('selected', "red4")])

# Create a Treeview Scrollbar
results_scroll = Scrollbar(results_frame)
results_scroll.place(relx=0.9782, rely=0.02, height=319)

# Create a Treeview widget to show Results
cols = ('SKU', 'Name', 'Type', 'Color',
        'Brand', 'Gender', 'Size', 'Price')
results = ttk.Treeview(results_frame, columns=cols, height=15,
                       show='headings', yscrollcommand=results_scroll.set, selectmode="extended")

for col in cols:
    results.heading(col, text=col)
    results.place(relx=0.01, rely=0.02)
    results.column(col, anchor=CENTER)
    if col == "SKU":
        results.column("SKU", minwidth=0, width=120)
    elif col == "Name":
        results.column("Name", minwidth=0, width=290)
    elif col == "Type":
        results.column("Type", minwidth=0, width=100)
    elif col == "Color":
        results.column("Color", minwidth=0, width=100)
    elif col == "Brand":
        results.column("Brand", minwidth=0, width=115)
    elif col == "Size":
        results.column("Size", minwidth=0, width=75)
    elif col == "Gender":
        results.column("Gender", minwidth=0, width=100)
    elif col == "Price":
        results.column("Price", minwidth=0, width=100)
    else:
        pass

# Configure the Scrollbar
results_scroll.config(command=results.yview)

# Create Striped Row Tags
results.tag_configure('oddrow', background="white")
results.tag_configure('evenrow', foreground="white", background="coral3")

# Label for Application Title
title_label = Label(root, text="ShoeSort Inventory Management", bg='white',
                    font="LemonMilk-Medium 32 bold", fg="red4").place(relx=.5, rely=0.06, anchor="center")


# Create a photoimage object
image1 = Image.open('icon.png').resize((70, 70), Image.ANTIALIAS)
icon = ImageTk.PhotoImage(image1)
shoesort_icon = Label(root, image=icon, bg='white')
shoesort_icon.image = icon

# Position image
shoesort_icon.place(relx=.02, rely=0)

# Create Text Boxes and Text Box Labels
# SKU text and label
sku = StringVar()
shoe_sku = Entry(root, width=30, bg='white smoke', textvariable=sku)
shoe_sku.place(relx=0.09, rely=0.16)
shoe_sku.bind("<KeyRelease>", caps)
shoe_sku_label = Label(root, text="SKU", font="BigNoodleTitling", bg='white')
shoe_sku_label.place(relx=0.03, rely=0.16)

# Shoe Name text box and label
shoe_name = Entry(root, width=30, bg='white smoke')
shoe_name.place(relx=0.09, rely=0.208)
shoe_name_label = Label(root, text="Name",
                        font="BigNoodleTitling", bg='white')
shoe_name_label.place(relx=0.03, rely=0.208)

# Shoe Brand text box and label
shoe_brand = Entry(root, width=30, bg='white smoke')
shoe_brand.place(relx=0.09, rely=0.256)
shoe_brand_label = Label(root, text="Brand",
                         font="BigNoodleTitling", bg='white')
shoe_brand_label.place(relx=0.03, rely=0.256)

# Shoe Type text box and label
shoe_type = StringVar()
shoe_type.set('')  # set the default option
typeMenu = OptionMenu(root, shoe_type, 'Running', 'Lifestyle', 'Trail Running/Hiking',
                      'Basketball', 'Volleyball', 'Football', 'Golf', 'Tennis', 'Training', 'Sandals/Slides')
typeMenu.place(relx=0.09, rely=0.295)
typeMenu.config(width=24)
shoe_type_label = Label(root, text="Type",
                        font="BigNoodleTitling", bg='white')
shoe_type_label.place(relx=0.03, rely=0.3)

# Shoe Size text box and label
shoe_size = StringVar(root)
shoe_size.set('')  # set the default option
sizesMenu = OptionMenu(root, shoe_size, '6', '7',
                       '8', '8.5', '9', '9.5', '10', '11', '12', '13')
sizesMenu.place(relx=0.345, rely=0.149)
sizesMenu.config(width=24)
shoe_size_label = Label(root, text="Size",
                        font="BigNoodleTitling", bg='white')
shoe_size_label.place(relx=0.290, rely=0.16)

# Shoe Color text box and label
shoe_color = StringVar(root)
shoe_color.set('')  # set the default option
colorMenu = OptionMenu(root, shoe_color, 'White', 'Black', 'Grey', 'Green',
                       'Blue', 'Navy', 'Orange', 'Red', 'Yellow', 'Pink',
                       'Purple', 'Brown', 'Cream', 'Mulitcolor')
colorMenu.place(relx=0.345, rely=0.249)
colorMenu.config(width=24)
shoe_color_label = Label(root, text="Color",
                         font="BigNoodleTitling", bg='white')
shoe_color_label.place(relx=0.290, rely=0.256)

# Gender text box and label
shoe_gender = StringVar(root)
shoe_gender.set('')  # set the default option
genderMenu = OptionMenu(root, shoe_gender, 'Male', 'Female')
genderMenu.place(relx=0.345, rely=0.199)
genderMenu.config(width=24)
shoe_gender_label = Label(root, text="Gender",
                          font="BigNoodleTitling", bg='white')
shoe_gender_label.place(relx=0.290, rely=0.205)

# Price text box and label
shoe_price = Entry(root, width=30, bg='white smoke')
shoe_price.place(relx=0.348, rely=0.3)
shoe_price_label = Label(
    root, text="Price", font="BigNoodleTitling", bg='white')
shoe_price_label.place(relx=0.292, rely=0.3)

# Search label
search_label = Label(search_frame, text="Search for item",
                     font="BigNoodleTitling 14", bg="coral1", fg="white")
search_label.place(relx=0.5, rely=0.2, anchor="center")

# Search SKU text box and label
search_sku = StringVar()
shoe_search = Entry(search_frame, width=30,
                    bg='white smoke', textvariable=search_sku)
shoe_search.place(relx=0.55, rely=0.45, anchor="center")
shoe_search.bind("<KeyRelease>", caps)
shoe_search_label = Label(
    search_frame, text="SKU", font="BigNoodleTitling", bg="coral1", fg="white")
shoe_search_label.place(relx=0.15, rely=0.45, anchor="center")

pity_label = Label(root, text="Sir, napuyat po kami dito. 'Wag niyo po kami ibagsak. Pls, ty :>",
                   font="calibri 7", bg='white')
pity_label.place(relx=0.5, rely=0.985, anchor="center")

# Create Buttons
# Create an Add Button
submit_btn = Button(root, text="Add Record", width=15,
                    font="BigNoodleTitling", bg="coral1", command=submit)
submit_btn.place(relx=0.075, rely=0.35)

# Create an Edit Button
edit_btn = Button(root, text="Update Record", width=15,
                  font="BigNoodleTitling", bg="coral1", command=update)
edit_btn.place(relx=0.185, rely=0.35)

# Create an clear Button
clear_btn = Button(root, text="Clear Entries", width=15,
                   font="BigNoodleTitling", bg="coral1", command=clear)
clear_btn.place(relx=0.295, rely=0.35)

# Create a Delete Button
delete_btn = Button(root, text="Delete Record", width=15,
                    font="BigNoodleTitling",  bg="coral1", command=delete)
delete_btn.place(relx=0.405, rely=0.35)

# Create a Select button
select_btn = Button(results_frame, text="Select Record", width=20,
                    font="BigNoodleTitling",  bg="red4", fg="white", command=select)
select_btn.place(relx=0.02, rely=0.9)

# Create a Show All Records Button
show_all_btn = Button(results_frame, text="Show All", width=20,
                      font="BigNoodleTitling", bg="red4", fg="white", command=show)
show_all_btn.place(relx=.7, rely=0.9)

# Create a Delete All Records Button
del_all_btn = Button(results_frame, text="Delete All", width=20,
                     font="BigNoodleTitling", bg="red4", fg="white", command=del_all)
del_all_btn.place(relx=.85, rely=0.9)

# Create a Search Button
search_btn = Button(search_frame, text="Search", width=15,
                    font="BigNoodleTitling", bg="red4", fg="white", command=search)
search_btn.place(relx=0.5, rely=0.75, anchor="center")


query_database()

root.mainloop()
