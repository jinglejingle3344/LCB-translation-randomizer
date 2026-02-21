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

window = tk.Tk(className='EVIL limbus text randomizer')
wtf = tk.Frame(window)
wtf.grid()
if not (platform in ('linux', 'win32')):
    txt = tk.Label(wtf, text='why are you using this on something other than bare linux or bare windows Friend')
    txt.grid()
    tk.Button(wtf, text='ok i get it i wont try it again',command=quit).grid()
    window.mainloop()
randomizeNames = tk.IntVar(wtf,value=1)
namis = ('teller', 'title','name')
dementia = tk.IntVar(wtf,value=0)
trySimilarSize = tk.IntVar(wtf,value=0)
topick = tk.StringVar(wtf,value='1')
delv = tk.IntVar(wtf,value=1)

randombsgo = ( # list of fields that can be just about any string value; used to grab all possible values and to 
#figure out which ones to scramble
#feel free to commen some out
    'desc', 
    'dlg', 
    'name', 
    'dialog',
    'content', 
    'teller',
    'title', 
    'abName', 
    'summary',
    'parttitle',
    'sentence',
    'flavor',
    'specialName',
    'variation2',
    #'usage',
    'shortName',
    'chapterNumber',
    'company',
    'nameWithTitle',
    #'subText',
    'openCondition',
    'mainText',
    'rawDesc',
    'teacher',
    'chapterTitle',
    'description', 
    'lowMoraleDescription', 
    'panicDescription',
    'panicName',
    'eventDesc',
    'behaveDesc',
    'simpleDesc',
    'prevDesc',
    'message',
    'result',
    'subDesc',
    'clue',
    'story',
    'codeName',
    #'messageDesc',
    'place',
)

vals = []

def obfuscate(v):
    nv=''
    for i in v:
        nv+=i if (randint(1, 10) <= 6) else '🤣'
    return nv

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
                if (i in randombsgo):
                    vals.append(g)
            else:
                vals.append(g)

def pickVal(original, i, recurse=0): #the value picker
    n = randint(0, len(vals)-1)
    v = vals[n]
    retries = 0
    origlen = len(original)
    while not (int(origlen*0.75) < len(v) < int(origlen*1.25)) and retries <= 24:
        n = randint(0, len(vals)-1)
        v = vals[n]
        retries+=1
    if delv.get() and recurse==0: del vals[n]
    if not randomizeNames.get() and i in namis: v = original
    if dementia.get() and i in namis: v = obfuscate(v)
    if recurse>0: v += ' '+pickVal(original,i,recurse-1)
    return v

def scrambleValues(obj): #crawl object for matching keys (fields), grab and remove valid values from vals, 
    #replace values at specific keys with picked value 
    if type(obj) is dict:
        obj1 = obj.items()
    elif type(obj) is list:
        obj1 = enumerate(obj)
    for i,v in obj1:
        isstr = type(v) is str
        if isinstance(v, Iterable) and not isstr:
            obj[i] = scrambleValues(v)
        elif isstr:
            recurse = list(map(int, topick.get().split('~')))
            if len(recurse)>1:
                recurse = randint(recurse[0], recurse[1]+1)
            else:
                recurse = recurse[0]
            bouttaadd = pickVal(v,i,recurse-1)
            if type(obj) is dict:
                if i in randombsgo:
                    obj[i] = bouttaadd
            else:
                obj[i] = bouttaadd
    return obj

def crawlFS(root, mode = 'r'): #crawl the filesystem for all text files to absolutely slaughter or to harvest their values
    if mode == 'w':
        for f in root.iterdir():
            if ('.otf' in f.name) or ('.ttf' in f.name) or ('.eot' in f.name) or ('.woff' in f.name) or ('.git' in f.name) or ('.vscode' in f.name): continue
            if f.is_dir():
                crawlFS(f, mode)
            else:
                if not ('.json' in f.name): continue
                lded = load(copen(f, 'r', 'utf-8-sig'))
                todump = scrambleValues(lded)
                absp = str(f.absolute())
                tounlink = ('EN_' in absp) or ('JP_' in absp) or ('KR_' in absp)
                dump(todump, copen(absp.replace('EN_', '').replace('JP_', '').replace('KR_', ''), 'w', 'utf-8-sig')) # there is likely 
                #a better way to rename the files. im just too lazy
                if tounlink: f.unlink()
    elif mode == 'r':
        for f in root.iterdir():
            if ('.otf' in f.name) or ('.ttf' in f.name) or ('.eot' in f.name) or ('.woff' in f.name) or ('.git' in f.name) or ('.vscode' in f.name): continue
            if f.is_dir():
                crawlFS(f, mode)
            else:
                if not ('.json' in f.name): continue
                harvestValues(load(copen(f, 'r', 'utf-8-sig')))
    elif mode == 'c':
        for f in root.iterdir():
            if ('.otf' in f.name) or ('.ttf' in f.name) or ('.eot' in f.name) or ('.woff' in f.name) or ('.git' in f.name) or ('.vscode' in f.name): continue
            if f.is_dir():
                crawlFS(f, mode)
            else:
                if not (('.json' in f.name) or ('.txt' in f.name) or ('.md' in f.name)): 
                    print(f.name)
                    tm.showerror('beware', 'you are making a horrible mistake by not picking a valid localization folder...\nOr the program fucked up. Sorry if such is the case') 
                    raise ValueError("horrible fate...")
# TK HELL
folds = ['','', '']
foldErr = 'you need to select folders'
langErr = 'you need to generate a new language'
topickError = 'is the text box empty? does it have a whole number in it? is it larger than 0?'
valErr = 'you need to grab values'
normalStatus = 'This tool may take a while to finish. Read the title bars of the file selector windows!'

status = tk.Label(wtf, text=normalStatus); status.grid()
infl1 = tk.Label(wtf, text='Selected localization files: None'); infl1.grid()
infl2 = tk.Label(wtf, text='Selected destination: None'); infl2.grid()
infl3 = tk.Label(wtf, text='Working with language folder: None'); infl3.grid()

def checktopick():
    txt1: str = topick.get().split('~')
    f = True
    for n in txt1:
        if not n.isdigit() or n == '0':
            f = False
            break
    return f

def selectfolds():
    if not checktopick():
        tm.showerror('Error', topickError) 
        return
    folds[0] = td.askdirectory(title='Go into the original localization files')
    crawlFS(Path(folds[0]), 'c')
    infl1['text'] = 'Selected localization files: '+str(folds[0])
    folds[1] = td.askdirectory(title='Go into the limbus company Lang folder')
    infl2['text'] = 'Selected destination: '+str(folds[1])

def copp():
    if not checktopick():
        tm.showerror('Error', topickError) 
        return
    if (folds[0] in ('', None, ())) or (folds[1] in ('', None, ())): 
        tm.showerror('Error', foldErr) 
        return
    fp = Path(folds[1])/('RNGLang'+str(randint(100000,999999)))
    copytree(folds[0], fp)
    folds[2] = str(fp)
    infl3['text'] = 'Working with language folder: '+folds[2]
    if not Path(folds[2]+'/Font').exists(): copytree('./Font', folds[2]+'/Font')
    
def grabvals():
    if not checktopick():
        tm.showerror('Error', topickError) 
        return
    if (folds[0] in ('', None, ())) or (folds[1] in ('', None, ())): 
        tm.showerror('Error', foldErr) 
        return
    vals.clear()
    crawlFS(Path(folds[0]))

def scramble():
    if not checktopick():
        tm.showerror('Error', topickError) 
        return
    if (folds[2] in ('', None, ())): 
        tm.showerror('Error', langErr) 
        return
    if (len(vals) == 0): 
        tm.showerror('Error', valErr) 
        return
    status['text'] = 'scrambling, window is probably unresponsive...'
    window.update()
    crawlFS(Path(folds[2]), 'w')
    status['text'] = normalStatus

def updconf():
    if not checktopick():
        tm.showerror('Error', topickError) 
        return
    if (folds[0] in ('', None, ())) or (folds[1] in ('', None, ())): 
        tm.showerror('Error', foldErr) 
        return
    if (folds[2] in ('', None, ())): 
        tm.showerror('Error', langErr) 
        return
    f = open(folds[1]+'/config.json', mode='w')
    f.write('''{
    "lang": "'''+Path(folds[2]).name+'''",
    "titleFont": "",
    "contextFont": "",
    "samplingPointSize": 78,
    "padding": 5
}
''')
    f.close()

def alloem():
    if not checktopick():
        tm.showerror('Error', topickError) 
        return
    selectfolds()
    copp()
    grabvals()
    scramble()
    updconf()

tk.Button(wtf, text='Select folders (make sure the path ends with /Lang for the second selector)', command=selectfolds).grid()
tk.Button(wtf, text='Make a copy of original, drop it at Lang with random name, add font folder (if needed; required to scramble)', command=copp, height=1).grid()
tk.Button(wtf, text='Grab all possible values from input folder', command=grabvals).grid()
tk.Button(wtf, text='Scramble values in working dir using values from ^', command=scramble).grid()
tk.Button(wtf, text='Update Lang configs (to not have to select the doohickey)', command=updconf).grid()
tk.Button(wtf, background="green", text='Dude i dont fucking care (complete every step at once; use this if you dont plan on messing with the above)', command=alloem).grid()
tk.Checkbutton(wtf, text='Dementia', variable=dementia).grid()
tk.Checkbutton(wtf, text='Randomize Names', variable=randomizeNames).grid()
tk.Checkbutton(wtf, text='Delete harvested values after use (being placed into a random field)\nDO set this to false if the input box below has a number > 1, or a range of numbers', variable=delv).grid()
tk.Label(wtf, text='How many times to add a random string to the field?\nSeparate 2 numbers with ~ to make it random (like 2~5)').grid()
tk.Entry(wtf, textvariable=topick).grid()
tk.Checkbutton(wtf, text='try to pick values of similar length to original. makes the process take longer since it rerolls 25 times', variable=trySimilarSize).grid()

window.mainloop()
