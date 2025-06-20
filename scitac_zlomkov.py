
class Error:
    def __init__(self, msg, line = None):
        self.msg = msg
        self.line = line

#
# Functions
#

def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

def lcm(a, b):
    if a == 0:
        return None
    return (a * b) // gcd(a, b)

def frac_validate(frac):
    if len(frac) != 2 \
            or type(frac[0]) is not int \
            or type(frac[1]) is not int:
        return Error("Chyba")
    if frac[1] == 0:
        return Error("Delenie nulou")
    return frac

def frac_norm(frac):
    frac = frac_validate(frac)
    if type(frac) is Error:
        return frac

    div = gcd(frac[0], frac[1])
    return [frac[0] // div, frac[1] // div]

def frac_add(frac1, frac2):
    frac1 = frac_validate(frac1)
    if type(frac1) is Error:
        return frac1

    frac2 = frac_validate(frac2)
    if type(frac2) is Error:
        return frac2

    mul = lcm(frac1[1], frac2[1])
    if mul is None:
        return Error("Delenie nulou")

    nom1 = frac1[0] * (mul // frac1[1])
    nom2 = frac2[0] * (mul // frac2[1])

    if mul == 0:
        return Error("Delenie nulou")
    frac = [nom1 + nom2, mul]
    return frac_norm(frac)

def fracs_sum(fracs):
    sum = [0, 1]
    for i, frac in enumerate(fracs):
        frac = frac_validate(frac)
        if type(frac) is Error:
            frac.msg += f" v zlomku: {i + 1}"
            frac.line = i + 1
            return frac

        sum = frac_add(sum, frac_norm(frac))
    return sum

def parse_fracs_string(fs: str):
    fracs = []
    # remove unnecessary whitespace
    fs = fs.strip().strip(" ").strip("\t")
    for i, line in enumerate(fs.split("\n")):
        try:
            frac = [int(e) for e in line.split("/")]
            frac = frac_validate(frac)
            if type(frac) is Error:
                frac.msg += f" v zlomku: {i + 1}"
                frac.line = i + 1
                return frac

            fracs.append(frac)
        except ValueError:
            return Error(f"Nesprávny formát na riadku: {i + 1}", line=(i + 1))
    return fracs

def build_fracs_string(fracs):
    fs = ""
    for frac in fracs:
        fs += f"{frac[0]}/{frac[1]}\n"
    return fs

def read_fracs_file(path):
    try:
        f = open(path, "r")
        fracs = parse_fracs_string(f.read())
        f.close()
        return fracs
    except:
        return Error("Nesprávny formát súboru")

#
# UI stuff
#

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tklinenums import TkLineNumbers
from pathlib import Path

root = TkinterDnD.Tk()
root.title("Súčet zlomkov")

log_sv = tk.StringVar()
error = None

def on_log_pressed(e):
    if error.line is None:
        return

    fracs_tb.see(f"{error.line:.1f}")
    fracs_tb.mark_set("insert", f"{error.line}.0")
    fracs_ln.redraw()

def on_key_pressed(e):
    global error

    if e.keysym == "KP_Enter":
        fracs_tb.insert("end", "\n")
        fracs_ln.redraw()
        return

    log_sv.set("")

    fracs = parse_fracs_string(fracs_tb.get(1.0, "end"))
    fracs_ln.redraw()

    if type(fracs) is Error:
        log_sv.set(f"Error: {fracs.msg}")
        error = fracs
        return

    frac = fracs_sum(fracs)
    if type(frac) is Error:
        log_sv.set(f"Error: {frac.msg}")
        error = frac
        return

    nom_label["text"] = frac[0]
    den_label["text"] = frac[1]

# drag'n'drop
def on_file_dropped(e):
    global error

    path = e.data
    log_sv.set(f"Súčet zlomkov z \"{Path(path).name}\"")

    fracs = read_fracs_file(path)
    if type(fracs) is Error:
        log_sv.set(f"Error: {fracs.msg}")
        error = fracs
        return

    fracs_tb.delete(1.0, "end")
    fracs_tb.insert("end", build_fracs_string(fracs))
    fracs_ln.redraw()

    frac = fracs_sum(fracs)
    if type(frac) is Error:
        log_sv.set(f"Error: {frac.msg}")
        error = frac
        return

    nom_label["text"] = frac[0]
    den_label["text"] = frac[1]

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_file_dropped)

# UI layout
display_frame = tk.Frame(master=root)

nom_label = tk.Label(master=display_frame, text="0")
nom_label.pack()

tk.Frame(master=display_frame, background="black").pack(fill="x")

den_label = tk.Label(master=display_frame, text="1")
den_label.pack()

display_frame.pack()

fracs_frame = tk.Frame(master=root)

fracs_sb = tk.Scrollbar(master=fracs_frame)
fracs_sb.pack(side="right", fill="y")

# input text
fracs_tb = tk.Text(master=fracs_frame, width=40, height=10)
fracs_tb.pack(side="right", expand=True, fill="both")
fracs_tb.bind_all("<Key>", on_key_pressed)

# line numbers
fracs_ln = TkLineNumbers(master=fracs_frame, textwidget=fracs_tb, justify="right", colors=("#2197db", "#ffffff"))
fracs_ln.pack(side="right", fill="y")

# Redraw the line numbers when the text widget contents are modified
fracs_tb.bind("<<Modified>>", lambda e: root.after_idle(fracs_ln.redraw), add=True)

# Link Scrollbar
def _yscroll_link(*args):
    fracs_sb.set(*args)
    fracs_ln.redraw()
fracs_sb.config(command=fracs_tb.yview)
fracs_tb.config(yscrollcommand=_yscroll_link)

fracs_frame.pack(expand=True, fill="both")

log_label = tk.Label(master=root, textvariable=log_sv)
log_label.pack(anchor="w", padx=10)
log_label.bind("<Button-1>", on_log_pressed)

# main loop
root.mainloop()
