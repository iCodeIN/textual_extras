# Textual-Extras


This is a hobby projects where I am building some usable widgets that could come in handy \
when building projects with textual (This project will most likely never merge in the original repo)


There is a repo that does the same kind of thing for inputs named - [textual_inputs](https://github.com/sirfuzzalot/textual-inputs) but... \
there were so many things i wanted to modify... so I created my own little library


## What is Textual?
[Textual](https://github.com/Textualize/textual) is a TUI (Text User Interface) framework for Python inspired by modern web development. Currently a Work in Progress.

> ⚠️ ***NOTE:*** Textual is going under rapid development and some things, at some point of time, might break.. \
> so PRs are more than welcome :)


## 💡 Widget Ideas:

<details>
  <summary> ✔️ Text Input </summary>
  
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
  - home => Moves cursor to the start of the text
  - end => Moves cursor to the end of the text
  - left/right arrow => Moves cursor by one position in the specified direction
  - ctrl + left/right => Moves cursor to the next space in the specified direction
  - backspace/delete => Delete one letter in the specified direction
  - ctrl + del => Delte a whole word to the right (Space serves as the delimiter)
  - ctrl + v => Paste the content from your system clipboard 
  
  > ⚠️ ***NOTE:*** There is no implementation for ctrl+backspace as backspace is represented as ctrl+h in textual and ctrl+ctrl+h, is unfortunately, not a thing :(
 
  > ⚠️ ***NOTE:*** ctrl+v should work just fine on windows and mac.. On linux if you are on X11 system.. consider adding `xclip` for this feature
  
</details>
