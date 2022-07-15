from main_model import engine, Ticket
from archyvas_model import variklis, Archive
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sqlite3
import random
import string

def default_values():
    id_entry.config(state="normal")
    id_entry.delete(0, END)
    id_entry.insert(END, id_gen())
    id_entry.config(state="readonly")
    date_entry.delete(0, END)
    date_entry.insert(END, str(datetime.today().date()))
    statusd_entry.delete(0, END)
    statusd_entry.insert(END, str(datetime.today().date()))
    status_entry.insert(END, status_entry.current(0))
    category_entry.insert(END, category_entry.current(0))
    owner_entry.insert(END, owner_entry.current(0))
    pav_entry.delete(0, END)
    desc_entry.delete(0, END)

def delete():
    Session = sessionmaker(bind=engine)
    w = Session()
    keiciamas_id = my_tree.focus()
    esamas = w.query(Ticket).get(keiciamas_id)
    w.delete(esamas)
    w.commit()
    status_bar["text"] = f"Record {id_entry.get()} deleted"
    my_tree.delete(*my_tree.get_children())
    query()
    default_values()

def archive():
    Session = sessionmaker(bind=variklis)
    s = Session()
    arch = Archive(id_entry.get(), pav_entry.get(), date_entry.get(), desc_entry.get(), status_entry.get(),
                   statusd_entry.get(), category_entry.get(), owner_entry.get())
    s.add(arch)
    s.commit()
    status_bar["text"] = f"Record {id_entry.get()} moved to archive"
    Session = sessionmaker(bind=engine)
    d = Session()
    keiciamas_id = my_tree.focus()
    esamas = d.query(Ticket).get(keiciamas_id)
    d.delete(esamas)
    d.commit()
    my_tree.delete(*my_tree.get_children())
    query()
    default_values()

def id_gen():
    rand_letter = random.choice(string.ascii_letters).upper()
    rand_int = random.randint(100000, 999999)
    return rand_letter + str(rand_int)

def query():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM Tickets")
    records = c.fetchall()
    count = 1
    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[2], record[3], record[4], record[5],
                                                                           record[6], record[7], record[8], record[9]))
        count += 1
    conn.commit()
    conn.close()

def add_record():
    Session = sessionmaker(bind=engine)
    s = Session()
    naujas = Ticket(id_entry.get(), pav_entry.get(), date_entry.get(), desc_entry.get(), status_entry.get(),
                    statusd_entry.get(), category_entry.get(), owner_entry.get())
    s.add(naujas)
    s.commit()
    status_bar["text"] = f"New rocord {id_entry.get()} added."
    my_tree.delete(*my_tree.get_children())
    query()
    default_values()

def select_record(e):

    id_entry.config(state='normal')
    id_entry.delete(0, END)
    pav_entry.delete(0, END)
    date_entry.delete(0, END)
    desc_entry.delete(0, END)
    status_entry.delete(0, END)
    statusd_entry.delete(0, END)
    category_entry.delete(0, END)
    owner_entry.delete(0, END)

    # Grab record Number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, 'values')

    id_entry.insert(0, values[0])
    id_entry.config(state='readonly')
    pav_entry.insert(0, values[1])
    date_entry.insert(0, values[2])
    desc_entry.insert(0, values[3])
    status_entry.insert(0, values[4])
    statusd_entry.insert(0, values[5])
    category_entry.insert(0, values[6])
    owner_entry.insert(0, values[7])

def update_record():
    Session = sessionmaker(bind=engine)
    s = Session()

    keiciamas_id = my_tree.focus()
    esamas = s.query(Ticket).get(keiciamas_id)
    esamas.rand_id = id_entry.get()
    esamas.pav = pav_entry.get()
    esamas.date = date_entry.get()
    esamas.desc = desc_entry.get()
    esamas.status = status_entry.get()
    esamas.status_date = statusd_entry.get()
    esamas.category = category_entry.get()
    esamas.emp = owner_entry.get()
    s.commit()

    selected = my_tree.focus()
    # Update record
    my_tree.item(selected, text="", values=(
        id_entry.get(), pav_entry.get(), date_entry.get(), desc_entry.get(), status_entry.get(),
        statusd_entry.get(), category_entry.get(), owner_entry.get(),))
    status_bar["text"] = f"Record {id_entry.get()} updated"
    default_values()

def archive_query():
    global archive_root
    archive_root = Tk()
    archive_root.title('Ticketing system - Archive')
    archive_root.geometry("1080x350")
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
    style.map('Treeview', background=[('selected', "#347083")])
    tree_frame = Frame(archive_root)
    tree_frame.pack(pady=10)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    global archive_tree
    archive_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    archive_tree.pack()
    tree_scroll.config(command=archive_tree.yview)
    archive_tree['columns'] = (
        "ID", "Title", "Date created", "Brief description", "Status", "Status date", "Category",
        "Owner")

    archive_tree.column("#0", width=0, stretch=NO)
    archive_tree.column("ID", anchor=W, width=55)
    archive_tree.column("Title", anchor=W, width=180)
    archive_tree.column("Date created", anchor=W, width=80)
    archive_tree.column("Brief description", anchor=W, width=220)
    archive_tree.column("Status", anchor=CENTER, width=100)
    archive_tree.column("Status date", anchor=CENTER, width=100)
    archive_tree.column("Category", anchor=CENTER, width=140)
    archive_tree.column("Owner", anchor=CENTER, width=140)

    archive_tree.heading("#0", text="", anchor=W)
    archive_tree.heading("ID", text="ID", anchor=CENTER)
    archive_tree.heading("Title", text="Title", anchor=CENTER)
    archive_tree.heading("Date created", text="Date created", anchor=CENTER)
    archive_tree.heading("Brief description", text="Brief description", anchor=CENTER)
    archive_tree.heading("Status", text="Status", anchor=CENTER)
    archive_tree.heading("Status date", text="Status date", anchor=CENTER)
    archive_tree.heading("Category", text="Category", anchor=CENTER)
    archive_tree.heading("Owner", text="Owner", anchor=CENTER)

    conn = sqlite3.connect('archyvas.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM Tickets")
    records = c.fetchall()
    count = 1
    for record in records:
        archive_tree.insert(parent='', index='end', iid=count, text='',
            values=(record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]))
        count += 1
    conn.commit()
    conn.close()

    in_archive_frame = LabelFrame(archive_root)
    in_archive_frame.pack(expand=YES, padx=20, pady=10)

    delete_arc_rec_btn = Button(in_archive_frame, text="Delete archive record", command=archive_delete)
    delete_arc_rec_btn.grid(row=0, column=0, padx=20, pady=10)

    restore_to_main_btn = Button(in_archive_frame, text="Move from archive to the main table",
                                 command=restore_from_archive)
    restore_to_main_btn.grid(row=0, column=1, padx=20, pady=10)

    global arc_status_bar
    arc_status_bar = Label(archive_root, text="Select action", bd=2, relief=SUNKEN, padx=30, pady=30)
    arc_status_bar.pack(fill="x")

    archive_root.mainloop()

def restore_from_archive():
    selected = archive_tree.focus()
    # Grab record values
    values = archive_tree.item(selected, 'values')
    Session = sessionmaker(bind=engine)
    d = Session()
    naujas = Ticket(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
    d.add(naujas)
    d.commit()
    my_tree.delete(*my_tree.get_children())
    query()
    archive_delete()
    arc_status_bar['text'] = f"Archyvo įrašas {values[0]} perkeltas į pagrindinį langą"
    status_bar['text'] = f"Įrašas {values[0]} grąžintas iš archyvo"

def archive_delete():
    Session = sessionmaker(bind=variklis)
    d = Session()
    keiciamas_id = archive_tree.focus()
    esamas = d.query(Archive).get(keiciamas_id)
    d.delete(esamas)
    d.commit()
    arc_status_bar['text'] = f"Archyvo įrašas {esamas.rand_id} ištrintas"
    archive_tree.delete(*archive_tree.get_children())
    archive_refresh()

def archive_refresh():
    conn = sqlite3.connect('archyvas.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM Tickets")
    records = c.fetchall()
    count = 1
    for record in records:
        archive_tree.insert(parent='', index='end', iid=count, text='', values=(record[2], record[3], record[4],
                record[5], record[6], record[7], record[8], record[9]))
        count += 1
    conn.commit()
    conn.close()


root = Tk()
root.title('Ticketing system')
root.geometry("1080x550")

style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Treeview', background=[('selected', "#347083")])
tree_frame = Frame(root)
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()
tree_scroll.config(command=my_tree.yview)
my_tree['columns'] = ("ID", "Title", "Date created", "Brief description", "Status", "Status date", "Category", "Owner")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=55)
my_tree.column("Title", anchor=W, width=180)
my_tree.column("Date created", anchor=CENTER, width=80)
my_tree.column("Brief description", anchor=W, width=220)
my_tree.column("Status", anchor=CENTER, width=100)
my_tree.column("Status date", anchor=CENTER, width=100)
my_tree.column("Category", anchor=CENTER, width=140)
my_tree.column("Owner", anchor=CENTER, width=140)
# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Title", text="Title", anchor=CENTER)
my_tree.heading("Date created", text="Date created", anchor=CENTER)
my_tree.heading("Brief description", text="Brief description", anchor=CENTER)
my_tree.heading("Status", text="Status", anchor=CENTER)
my_tree.heading("Status date", text="Status date", anchor=CENTER)
my_tree.heading("Category", text="Category", anchor=CENTER)
my_tree.heading("Owner", text="Owner", anchor=CENTER)

data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand=YES, padx=20)

id_label = Label(data_frame, text="Unique Number")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame)
generated_id = id_gen()
id_entry.insert(END, generated_id)
id_entry.grid(row=0, column=1, padx=10, pady=10)
id_entry.config(state='readonly')

pav_label = Label(data_frame, text="Title")
pav_label.grid(row=0, column=2, padx=10, pady=10)
pav_entry = Entry(data_frame, width=40)
pav_entry.grid(row=0, column=3, padx=10, pady=10)

date_label = Label(data_frame, text="Date created")
date_label.grid(row=0, column=4, padx=10, pady=10)
date_entry = DateEntry(data_frame, date_pattern='yyyy-mm-dd', width=18)
date_entry.grid(row=0, column=5, padx=10, pady=10)

desc_label = Label(data_frame, text="Brief description")
desc_label.grid(row=1, column=0, padx=10, pady=10)
desc_entry = Entry(data_frame, width=60)
desc_entry.grid(row=1, column=1, columnspan=3, padx=20, pady=10)

status = ['Assigned', 'In Progress', 'Escalated', 'Cancelled', 'On Hold', 'Completed']
statusVar = StringVar(data_frame)
statusVar.set(status[0])

status_label = Label(data_frame, text="Status")
status_label.grid(row=1, column=4, padx=10, pady=10)
status_entry = ttk.Combobox(data_frame, values=status)
status_entry.current(0)
status_entry.grid(row=1, column=5, padx=10, pady=10)
status_entry.config(width=15)

statusd_label = Label(data_frame, text="Status date")
statusd_label.grid(row=2, column=0, padx=10, pady=10)
statusd_entry = DateEntry(data_frame, date_pattern='yyyy-mm-dd', width=18)
statusd_entry.grid(row=2, column=1, padx=10, pady=10)

kategorijos = ['small issue', 'moderate issue', 'complex issue', 'No category']
catVar = StringVar(data_frame)
catVar.set(kategorijos[3])

category_label = Label(data_frame, text="Category", justify="right")
category_label.grid(row=2, column=2, pady=10)
category_entry = ttk.Combobox(data_frame, values=kategorijos, width=60)
category_entry.current(0)
category_entry.grid(row=2, column=3, pady=10)
category_entry.config(width=15)

zmones = ['Jonas Jonaitis', 'Petras Petraitis', 'Andrius Kazlauskas', 'Gitanas Nausėda']
zmVar = StringVar(data_frame)
zmVar.set(zmones[0])

owner_label = Label(data_frame, text="Owner")
owner_label.grid(row=2, column=4, padx=10, pady=10)
owner_entry = ttk.Combobox(data_frame, values=zmones)
owner_entry.current(0)
owner_entry.grid(row=2, column=5, padx=10, pady=10)
owner_entry.config(width=15)
#=====================FREIMAI===========================
bendras_frame = LabelFrame(root)
bendras_frame.pack(expand=YES, padx=20, pady=20)

button_frame = LabelFrame(bendras_frame)
button_frame.grid(row=0, column=0)

archive_frame = LabelFrame(bendras_frame)
archive_frame.grid(row=0, column=1)

additional_frame = LabelFrame(bendras_frame)
additional_frame.grid(row=0, column=6, columnspan=3, sticky=E)
#--------------------------------------------------------------------------------
add_button = Button(button_frame, text="Add a record", command=add_record)
add_button.grid(row=0, column=0, padx=20, pady=10)
root.bind('<Return>', lambda event: add_record())

update_button = Button(button_frame, text="Update the record", command=update_record)
update_button.grid(row=0, column=1, padx=20, pady=10)

archive_button = Button(archive_frame, text="Archive the record", anchor=E, command=archive)
archive_button.grid(row=0, column=2, padx=20, pady=10)

show_archive_button = Button(archive_frame, text="Archive", anchor=E, command=archive_query)
show_archive_button.grid(row=0, column=3, padx=20, pady=10)

reset_button = Button(additional_frame, text="Reset", anchor=E, command=default_values)
reset_button.grid(row=0, column=6, padx=20, pady=10)

delete_button = Button(additional_frame, text="Remove the record", anchor=E, command=delete)
delete_button.grid(row=0, column=7, padx=20, pady=10)

status_bar = Label(root, text="Select the action", bd=2, relief=SUNKEN, padx=30, pady=30)
status_bar.pack(fill="x")

query()
my_tree.bind("<ButtonRelease-1>", select_record)

root.mainloop()
