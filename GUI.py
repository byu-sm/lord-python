from tkinter import *

def show_entry_fields():
   print("COM_PORT: %s\nBS_BAUD: %s\nNODE_ADDR: %s" % (e1.get(), e2.get(), e3.get()))

master = Tk()
Label(master, text="COM_PORT").grid(row=0)
Label(master, text="BS_BAUD").grid(row=1)
Label(master, text="NODE_ADDR").grid(row=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)


Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

mainloop()
