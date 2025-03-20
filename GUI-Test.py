from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import tkinter

import encoding
import decompress


##########################################################################

ogSizeInt = "N/A"
cSizeInt = "N/A"
ratioStr = "N/A"

#huffmanCodeText = "Enter text by typing or loading a .txt file."
outPath = None
treePtr = None
filePath = ""

##########################################################################


#functions for retrieving 
def getFile():
    try:
        global filePath
        filePath = filedialog.askopenfilename()
        if filePath[len(filePath)-3:] != "txt":
            print("Not a proper .txt file")
            return
    
        with open(filePath, 'r') as file:
            textContent = file.read()
            return textContent
        
    except FileNotFoundError:
        print("Error oh no. Probably a pathing error")
    except:
        print("oopsies text no worky")


def getHuffmanTextFF(textEntry):
    try:
        textContent = ""
        with open("huffmanCodes.txt", 'r') as file:
            textContent = file.read()
        textEntry.config(state="normal")
        textEntry.delete('1.0', tkinter.END)
        textEntry.insert(tkinter.INSERT, textContent)
        textEntry.config(state="disabled")
    except:
        print("oops")


def getTextFF(textEntry):
    try:
        text = getFile()
        encoding.build_huffman_tree(text)
        textEntry.delete('1.0', tkinter.END)
        textEntry.insert(tkinter.INSERT, text)
    except:
        print("oh no")

def encodeText(textEntry, huffEntry, infoBox):
    global treePtr
    global outPath
    global ogSizeInt
    global cSizeInt
    global ratioStr
    global infoText

    text = textEntry.get("1.0", tkinter.END)
    treePtr = encoding.build_huffman_tree(text)
    outPath = encoding.getHFFMCodes(text)

    ogSizeInt = encoding.original_size
    cSizeInt = encoding.compressed_bytes
    ratioStr = encoding.compression_percentage

    infoBox.config(text=f"OG Size: {ogSizeInt} bytes | Compressed Size: {cSizeInt} bytes | Ratio: {ratioStr:.2f}%")
    print()

    getHuffmanTextFF(huffEntry)

def decompressText(textEntry):
    try:
        newText = encoding.decompress_file("compressedBinary.txt", treePtr)
        textEntry.config(state="normal")
        textEntry.delete('1.0', tkinter.END)
        textEntry.insert(tkinter.INSERT, newText)
        textEntry.config(state="disabled")
    except:
        print("no decompress")

########################################



#main windows containter
root = tkinter.Tk(className="Huffman Encoder")
root.configure(bg='#00008B')
root.minsize(940, 800)
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)


#styling for the main window and text
style = ttk.Style()
style.configure("W.TFrame", background="#00008B")
style.configure("W.TLabel", foreground='white', background="#00008B", font=("Arial", 40, "bold"))
style.configure("sW.TLabel", foreground='white', background="#00008B", font=("Arial", 20))


###################################################################################################

mainLabel = ttk.Label(root, text="Huffman Encoding Tool",style='W.TLabel', anchor='center').grid(column=0, row=0)

###################################################################################################

#displays the og size, compressed size, and the percentage of compression compared to the original
infoTextBox = ttk.Label(root, text=f"OG Size: {ogSizeInt} bytes | Compressed Size: {cSizeInt} bytes | Ratio: {ratioStr}%", style='sW.TLabel', anchor='center')
infoTextBox.grid(column=0, row=1,padx=14)

#button frames for holding multiple buttons on the same row
buttonFrame = ttk.Frame(root,padding=5, style='W.TFrame')
buttonFrame.grid()
buttonFrame.grid_columnconfigure(0, weight=1)

#first two scroll text boxes
huffmanCodesTextBox = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=8)
huffmanCodesTextBox.grid(column=0, row=6, pady=10)
huffmanCodesTextBox.config(state="disabled")
entryE = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=8)
entryE.grid(column=0, row=3, pady=10)

loadFile = ttk.Button(buttonFrame, text="Load Text To Encode File", command=lambda: getTextFF(entryE)).grid(column=1, row=2, padx=14)

encode = ttk.Button(buttonFrame, text="Encode", command=lambda: encodeText(entryE, huffmanCodesTextBox, infoTextBox)).grid(column=0, row=2)

#huffman section of gui
##########################################################################

huffmanCodesLabel = ttk.Label(root, text='HuffmanCodes', style='sW.TLabel', anchor='center').grid(column=0, row=4)

huffmanCodesTextBox = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=8)
huffmanCodesTextBox.grid(column=0, row=6, pady=10)
huffmanCodesTextBox.config(state="disabled")

#decode section of gui
##########################################################################
#decode text box
entryD = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=8)
entryD.grid(column=0, row=8, pady=10)
entryD.config(state="disabled")

decode = ttk.Button(root, text="Decode", command=lambda: decompressText(entryD)).grid(column=0, row=7)


quitButton = ttk.Button(root, text="Quit", command=root.destroy).grid(column=0, row=9)


root.mainloop()

