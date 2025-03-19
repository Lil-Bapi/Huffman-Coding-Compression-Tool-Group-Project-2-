from tkinter import * 
from tkinter import ttk
from tkinter import scrolledtext
import tkinter

# import encoding
# import decompress


#main windows containter
root = Tk(className="Huffman Encoder")
root.configure(bg='#00008B')
root.minsize(940, 700)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)



style = ttk.Style()
style.configure("W.TFrame", background="#00008B")
style.configure("W.TLabel", foreground='white', background="#00008B", font=("Arial", 20, "bold"))
style.configure("sW.TLabel", foreground='white', background="#00008B", font=("Arial", 10))


##########################################################################
inputText = StringVar()


mainLabel = ttk.Label(root, text="Huffman Encoding Tool",style='W.TLabel', anchor='center').grid(column=0, row=0)


loadedFileName = ttk.Label(root, text="No file loaded...", style='sW.TLabel', anchor='center').grid(column=0, row=1)

buttonFrame = ttk.Frame(root,padding=5, style='W.TFrame')
buttonFrame.grid()
buttonFrame.grid_columnconfigure(0, weight=1, )
loadFile = ttk.Button(buttonFrame, text="Load Text File", command=root.destroy).grid(column=1, row=2)
encode = ttk.Button(buttonFrame, text="Encode", command="").grid(column=0, row=2)


#encode textbox
entryE = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=3).grid(column=0, row=3)


##########################################################################

decode = ttk.Button(root, text="Decode", command=root.destroy).grid(column=0, row=4)

#decode text box
entryD = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=4).grid(column=0, row=5)

quitButton = ttk.Button(root, text="Quit", command=root.destroy).grid(column=0, row=6)


root.mainloop()

