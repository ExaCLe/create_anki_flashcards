import tkinter as tk
from tkinter.filedialog import askopenfilename
from createFlashCards import read_in_cards
import sys


def chooseFile():
    file = askopenfilename()
    read_in_cards(file)
    sys.exit(0)

def main():
    window = tk.Tk()
    button = tk.Button(text="Choose File", command=chooseFile)
    button.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
