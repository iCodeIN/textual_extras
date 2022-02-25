# Textual-Extras


This is a hobby projects where I am building some usable widgets that could come in handy \
when building projects with textual (This project will most likely never merge in the original repo)


There is a repo that does the same kind of thing for inputs named - [textual_inputs](https://github.com/sirfuzzalot/textual-inputs) but... \
there were so many things i wanted to modify... so I created my own little library


## What is Textual?
[Textual](https://github.com/Textualize/textual) is a TUI (Text User Interface) framework for Python inspired by modern web development. Currently a Work in Progress.

> ⚠️ ***NOTE:*** Textual is going under rapid development and some things, at some point of time, might break.. \
> so PRs are more than welcome :)

# Installation

## One Liner
```bash
python -m pip install git+https://github.com/kraanzu/textual-extras.git
```

## Or if you prefer Manual Installation
``` bash
git clone https://github.com/kraanzu/textual-extras.git
cd termtyper
pip install .
```


## 💡 Widget Ideas:

<details>
  <summary> ✔️ <b>Text Input</b> </summary>
  
  ### A Simple, Single Line Text Input Box
  ------------------
  ### Features: 
  - [x] Provides a movable view with the cursor so that user experince is great
  - [x] Have shortcuts for smooth travelling in the input area (see at the end of the section for more details)
  - [x] Support for placeholders and title customization
  - [x] Support for password protected texts
  - [x] Movable view with respect to the cursor
  - [ ] Inline Syntax highlighing
  - [ ] Inline passwords
  - [ ] Simultaneous update of rich markup
  
  ------------------
  ### Controls
  - **home** => Moves cursor to the start of the text
  - **end** => Moves cursor to the end of the text
  - **left/right arrow** => Moves cursor by one position in the specified direction
  - **ctrl + left/right** => Moves cursor to the next space in the specified direction
  - **backspace/delete** => Delete one letter in the specified direction
  - **ctrl + del** => Delte a whole word to the right (Space serves as the delimiter)
  - **ctrl + v** => Paste the content from your system clipboard 
  
  > ⚠️ ***NOTE:*** There is no implementation for ctrl+backspace as backspace is represented as ctrl+h in textual and ctrl+ctrl+h, is unfortunately, not a thing :(
 
  > ⚠️ ***NOTE:*** ctrl+v should work just fine on windows and mac.. On linux if you are on X11 system.. consider adding `xclip` for this feature
  **On Ubuntu :** sudo apt install xclip \
  **On ArchLinux :** well you should know it already if you use Arch.. I use Arch btw :) 
  
</details>

<details>
  <summary> ✔️ <b>Number Input</b> </summary>
  
  ### A Simple, Single Line Number Input Box.. 
  ------------------
  ### Features: 
  - Same as Text Input

</details> 

<details>
  <summary> ⚠️(WIP) <b>Mutli-Line Input</b> </summary>
  
  ### A Simple, Mutli Line Code Input Box with syntax highlighting.. 
  ------------------
  ### Features: 
  - TODO

</details> 

<details>
  <summary> ⚠️(WIP) <b>Syntax Box</b> </summary>
  
  ### A Simple, Mutli Line Number Input Box.. 
  ------------------
  ### Features: 
  - TODO

</details> 


<details>
  <summary> ⚠️(WIP) <b>List</b> </summary>
  
  ### A List View to show, add, delete and modify items.. 
  ------------------
  ### Features: 
  - TODO

</details> 

<details>
  <summary> ⚠️(WIP) <b>Searchable List</b> </summary>
  
  ### A List with a bar to search for items in the list.. 
  ------------------
  ### Features: 
  - TODO

</details> 
