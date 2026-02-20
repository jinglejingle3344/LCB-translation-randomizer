# LCB-translation-randomizer
Simple python script with a GUI to randomize Limbus Company's localization
<img width="927" height="440" alt="image" src="https://github.com/user-attachments/assets/0cd7ffdb-d7ff-4086-b786-4971369c18b3" />


# Installation (if you dont use github Ever)

1. install python [here](https://www.python.org/downloads/)
1. click the gigantic Code button on the top right
2. download as zip
3. unpack
4. Enjoy!
5. optionally remove the files, they arent needed since it just creates a new localization folder

# Usage

- this works on both linux and windows. i dont have a mac to test it there which is why it wont even start for mac users, sorry  
- on windows, run it by double-clicking the .pyw file, on linux you can configure your system to also support that or you can use the terminal in the folder  
- it comes bundled with the original english localization; you can easily find it in the game's files (you can find it at `~/.local/share/Steam/steamapps/common/Limbus Company/LimbusCompany_Data/Assets/Resources_moved/Localize` on linux, on windows you'll have to look for it, though it should also be in steamapps) when this one becomes outdated  
- the buttons really should explain all you need to know  
    - the lang folder the program speaks of is located at `~/.local/share/Steam/steamapps/common/Limbus Company/LimbusCompany_Data/Lang` on linux (presumably depends on where you installed limbus)
- on windows you can simply select the target folders, i think  

# how it works (dont read if uninterested, its just file manipulation)

it simply memorizes the first folder as the input localization folder and the second as the output lang folder  
the next step is copying the original folder's contents to a new folder with a randomized name located in lang while also putting in the font folder (it does not overwrite any existing fonts, incase this is applied to a custom localization; a font is required for limbus to be able to load a custom language)  
then, it scans every json file in the input folder to find each string that corresponds to valid text fields (which are listed in a tuple) and puts them into a list  
having done that, it then goes through the new copy of the folder located at lang, updates every field with a completely random string from the list obtained from the previous step (while removing used up strings from the list, so that there arent any repeats), strips the files of any localization prefixes (EN_, KR_, JP_; stripping these is required for limbus to be capable of reading the new localization) and saves them. this is the most time consuming step  
afterwards, it simply updates the config.json file to tell limbus to use the new localization file and thats that  
<br>
the reason i let people complete each step individually is so that they can try to mix and match things for potentially an even more humorous experience
<br>
this project should remain dependency-less, because otherwise it'll have to be compiled into an executable for the convenience of the average joe. this, as you may be acutely aware, obfuscates the source code, allowing me to realistically put anything into the program and eroding trust
<br><br>
this is my first public project, so expect some really strange and questionable code
