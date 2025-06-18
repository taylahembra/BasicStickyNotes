#### StickyNotes ####
# An app that allows you to save stickynotes
# Saves all text in text files in the program's notes folder unencrypted
# You can add, remove, close and open stickynotes
# All removed stickynotes just get moved to the trash folder, and should be deleted manually

import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk
import shutil
import concurrent.futures

### Control Panel ###
class App(tk.Tk):
    def __init__(self, title, size, minSize=(0, 0), pool = None):
        # Main
        super().__init__()
        self.threads = pool
        self.title(title)
        self.idNum = 0
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(minSize[0], minSize[1])
        self.NoteObjects = list()

        # Stuff
        self.menu = Title(self)
        self.notes = Notes(self)

        self.loadNotes()

        self.mainloop()

    def addNote(self, title="New Note", text="", openNote=True, id = -1):
        print(f"Adding a new note, id {id} / {self.idNum}")


        if (id == -1):
            id = self.idNum + 1

        self.notes.addNote(id, title)

        if (openNote == True):
            ## Having errors here. Sometimes the function stops until program is shut down
            self.NoteObjects.append(Note(self.idNum + 1, title, (300, 400), (200, 200), self, text))
            # Not running until both windows are destroyed
            self.idNum += 1

        path = str(Path.cwd()) + "/Notes/info.txt"
        with open(path, "w") as f:
            f.write(f"{self.idNum}")

    def openNote(self, id):
        print(f"Opening note {id} / {self.idNum}")
        path = str(Path.cwd()) + "/Notes/" + str(id) + ".txt"
        with open(path) as f:
            fulltext = f.read().split("\n")
            title = fulltext[0]
            text = fulltext[1:]
            text = "\n".join(text)

        self.NoteObjects.append(Note(id, title, (300, 400), (200, 200), self, text))
        self.idNum += 1

    def loadNotes(self):
        # Path stuff
        path = Path.cwd()
        newPath = str(path) + "/Notes"

        # Create folder and info if it doesn't exist
        if not os.path.exists(newPath):
            print("Creating folder")
            os.mkdir("Notes")
        if not os.path.exists(str(path) + "/Trash"):
            print("Creating folder")
            os.mkdir("Trash")
        if not os.path.exists(newPath + "/info.txt"):
            print("Creating info file")
            with open(newPath + "/info.txt", "a") as f:
                f.write(f"{self.idNum}")
        else:
            with open(newPath + "/info.txt") as f:
                self.idNum = int(f.read())

        for i in next(os.walk(newPath))[2]:
            if i != "info.txt":
                with open(str(newPath) + "/" + i) as f:
                    fulltext = f.read().split("\n")
                    title = fulltext[0]
                    text = fulltext[1:]
                    text = "\n".join(text)
                    self.addNote(title, text, False, int(i.split(".txt")[0]))

class Title(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.columnconfigure(0, weight=15)
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="Notes:", font="30").grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        ttk.Button(self, text="+", command= lambda: self.parent.addNote(title="New Note", text="", openNote=True, id = -1)).grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.place(x=0, y=0, relwidth=1, height=50)


class Notes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place(x=0, y=50, relwidth=1, relheight=1)
        self.row = -1
        #self.noteObjects = list()
        self.noteLabels = {}

    def addNote(self, id, title="New Note"):
        self.row += 1
        self.rowconfigure(self.row, weight=1)
        self.noteLabels[id] = NoteObject(self, title, id)

    def saveTitle(self, id, title):
        test = self.noteLabels[id].label
        test["text"] = title


class NoteObject(ttk.Frame):
    def __init__(self, parent, title, id):
        super().__init__(parent)
        self.id = id
        self.parent = parent
        self.columnconfigure(0, weight=10, uniform="Silent_Creme")
        self.columnconfigure(1, weight=1, uniform="Silent_Creme")
        self.columnconfigure(2, weight=1, uniform="Silent_Creme")
        self.label = ttk.Label(self, text = title)
        self.label.grid(row=0, column=0, sticky="nswe", padx=5)
        ttk.Button(self, text="o", command=lambda: self.parent.parent.openNote(id)).grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        ttk.Button(self, text="x", command=lambda: self.remove()).grid(row=0, column=2, sticky="nswe", padx=5, pady=5)
        self.pack(fill="both")

    def remove(self):
        # Delete UI object and move the file to the trash folder
        self.destroy()
        path = str(Path.cwd()) + f"/Notes/{self.id}.txt"
        newpath = str(Path.cwd()) + f"/Trash/{self.id}.txt"
        shutil.move(path, newpath)



#### Note ####
class Note(tk.Tk):
    def __init__(self, id, title, size, minSize=(0, 0), parent=None, text=""):
        # Main
        super().__init__()
        self.id = id
        self.parent = parent
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(minSize[0], minSize[1])

        # Stuff
        ##self.menu = NoteTitle(self, title, text)

        # Title
        self.titlevar = tk.StringVar()
        self.titlevar = title
        self.titleText = ttk.Entry(self, font="30", textvariable=self.titlevar)
        self.titleText.insert(tk.END, title)
        self.titleText.pack(fill="both")

        # Text
        self.text = tk.Text(self)
        self.text.insert(tk.END, text)
        self.text.pack(fill="both")
        self.bind("<FocusOut>", lambda event: self.saveText())
        self.bind("<Leave>", lambda event: self.saveText())

        self.mainloop()

    def saveText(self):
        path = str(Path.cwd()) + "/Notes/" + str(self.id) + ".txt"
        if not os.path.exists(path):
            with open(path, "a") as f:
                f.write(self.titleText.get() + "\n" + self.text.get('1.0', 'end-1c'))
        else:
            with open(path, "w") as f:
                f.write(self.titleText.get() + "\n" + self.text.get('1.0', 'end-1c'))
        self.parent.notes.saveTitle(self.id, self.titleText.get())



# Open app
pool = concurrent.futures.ThreadPoolExecutor(max_workers=1000)
App("StickNotes", (500, 700), (500, 300), pool)
