from Tkinter import *

app = Tk()
app.title("GroupEng")
app.geometry("550x600+200+200")

scrollbar = Scrollbar(app, orient=VERTICAL)
listbox = Listbox(app, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)

listbox.insert(END, "a list entry")
for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)


app.mainloop()