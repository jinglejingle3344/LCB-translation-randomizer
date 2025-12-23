from json import dump, load
from codecs import open as copen
from pathlib import Path
from collections.abc import Iterable
from sys import setrecursionlimit
from random import randint
from sys import platform
import tkinter as tk
import tkinter.filedialog as td
import tkinter.messagebox as tm
from shutil import copytree
setrecursionlimit(90000000)

window = tk.Tk(className='EVIL limbus json value dumper')
wtf = tk.Frame(window)
wtf.grid()
if not (platform in ('linux', 'win32')):
    txt = tk.Label(wtf, text='why are you using this on something other than bare linux or bare windows Friend')
    txt.grid()
    tk.Button(wtf, text='ok i get it i wont try it again',command=quit).grid()
    window.mainloop()
tFieldSave = tk.StringVar(wtf)
vals = []

def harvestValues(obj): #crawl object for matching keys (fields), put into vals
    if type(obj) is dict:
        obj1 = obj.items()
    elif type(obj) is list:
        obj1 = enumerate(obj)
    for i,g in obj1:
        isstr = type(g) is str
        if isinstance(g, Iterable) and not isstr:
            harvestValues(g)
        elif isstr:
            if type(obj) is dict:
                if i != tFieldSave.get(): continue
                vals.append(g)

def crawlFS(root, mode = 'r'): #crawl the filesystem for all text files to absolutely slaughter or to harvest their values
    for f in root.iterdir():
        if ('.otf' in f.name) or ('.ttf' in f.name) or ('.eot' in f.name) or ('.woff' in f.name) or ('.git' in f.name) or ('.vscode' in f.name): continue
        if f.is_dir():
            crawlFS(f, mode)
        else:
            if not ('.json' in f.name): continue
            harvestValues(load(copen(f, 'r', 'utf-8-sig')))
# TK HELL
folds = ['']
normalStatus = 'this thing is used strictly for debugging and finding out what each json key actually means'

status = tk.Label(wtf, text=normalStatus); status.grid()
infl1 = tk.Label(wtf, text='Selected localization files: None'); infl1.grid()

def selectfolds():
    folds[0] = td.askdirectory(title='Go into the original localization files')
    infl1['text'] = 'Selected localization files: '+str(folds[0])

def dumpFields():
    if folds[0] in (None, '', ()):
        tm.showerror('system files deleted in 3.. 2..', 'select folder idiot')
        return
    tFieldSave.set(targetField.get('1.0',"end-1c"))
    crawlFS(Path(folds[0]))
    newdump = open('dump'+str(randint(0,10000000000000))+tFieldSave.get()+'.txt', 'w')
    newdump.write('\n'.join(vals))
    newdump.close()
    vals.clear()

tk.Button(wtf, text='select folder', command=selectfolds).grid()
targetField = tk.Text(wtf, width=30, height=1); targetField.grid()
tk.Button(wtf, text='dump', command=dumpFields).grid()

window.mainloop()
