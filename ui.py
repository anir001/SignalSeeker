import sys
import os
from seeker.engine import Engine
from util.img_procces import merge_and_save
from util.to_pdf import save_to_pdf
from termcolor import colored
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

VER = 'v2.0.1'

PDF_OUTPUT_DIR = 'pdf_output'
TMP_DIR = 'tmp'


def browse_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_file_path.set(file_path)


def browse_to_find_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    to_find_file_path.set(file_path)


def start_search():
    path_pdf = pdf_file_path.get()
    path_to_find = to_find_file_path.get()
    start_page = start_page_entry.get()
    stop_page = stop_page_entry.get()

    if not os.path.exists(path_pdf):
        messagebox.showerror("Error", "Selected PDF file does not exist.")
        return

    if not os.path.exists(path_to_find):
        messagebox.showerror("Error", "Selected To Find file does not exist.")
        return

    try:
        start_page = int(start_page) - 1
        stop_page = int(stop_page)
    except ValueError:
        messagebox.showerror("Error", "Invalid start page or stop page.")
        return

    engine = Engine()

    signals = engine.run(path_pdf, path_to_find, start_page, stop_page)

    footer = f"Generated using SignalSeeker {VER} from a file {os.path.basename(path_pdf)}\nSignalSeeker is licensed under the GNU " \
             f"GENERAL PUBLIC LICENSE v3.0 "
    merge_and_save([x.get_screen() for x in signals], footer)

    print("PDF creating")

    save_to_pdf(os.path.basename(path_pdf))

    duplicates, missing = engine.validate()
    if duplicates:
        print(colored("Found duplicate signals:", 'yellow'))
        for d in duplicates:
            print(colored(f'# {d}', 'yellow'))
    if missing:
        print(colored("Signals not found:", 'red'))
        for m in missing:
            print(colored(f'# {m}', 'red'))

    messagebox.showinfo("Finish", "Finish OK")
    print(colored("Finish OK", 'green'))


root = Tk()
root.title(f"Signal Seeker {VER}")
root.geometry("400x275")

pdf_file_path = StringVar()
to_find_file_path = StringVar()

pdf_label = Label(root, text="PDF File:")
pdf_label.pack(pady=5)

pdf_frame = Frame(root)
pdf_frame.pack()

pdf_entry = Entry(pdf_frame, textvariable=pdf_file_path)
pdf_entry.pack(side=LEFT, padx=5)

pdf_button = Button(pdf_frame, text="Browse", command=browse_pdf_file)
pdf_button.pack(side=LEFT)

to_find_label = Label(root, text="To Find File:")
to_find_label.pack(pady=5)

to_find_frame = Frame(root)
to_find_frame.pack()

to_find_entry = Entry(to_find_frame, textvariable=to_find_file_path)
to_find_entry.pack(side=LEFT, padx=5)

to_find_button = Button(to_find_frame, text="Browse",
                        command=browse_to_find_file)
to_find_button.pack(side=LEFT)

start_page_label = Label(root, text="Start Page:")
start_page_label.pack(pady=5)

start_page_entry = Entry(root)
start_page_entry.pack()

stop_page_label = Label(root, text="Stop Page:")
stop_page_label.pack(pady=5)

stop_page_entry = Entry(root)
stop_page_entry.pack()

start_button = Button(root, text="Start", command=start_search)
start_button.pack(pady=10)

root.mainloop()
