from tkinter import *

class Window():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.overrideredirect(True)

        self.title = Label(self.root, text = "Hello World", font = ("Roboto", 24))
        self.close_button = Button(self.root, text = "Close", command = self.close)

        self.title.pack()
        self.close_button.pack()

        self.root.mainloop()

    def close(self):
        self.root.destroy()

if __name__ == '__main__':
    win = Window()