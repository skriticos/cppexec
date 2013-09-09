pyexec README
=============

This is a small application to paste/type a c/c++ snippet and execute it.
Useful for ad-hoc testing of smaller code fragments without much setup. Just
paste and run.

![alt tag](https://raw.github.com/skriticos/cppexec/master/cppexec.png)

### Usage

1.  paste or type c/c++ snipet in input box
2.  select compiler (c/cpp)
3.  run application with the run control (or Alt-r)
4.  see result in the output box

#### X11 Clipboard Fetch Startup

1.  run ./cppexec.py -xclip
2.  see X11 clipboard content in input and result in output

### Requirements

*   Linux       -- tested on Ubuntu 12.04
*   Python 3    -- it's a python 3 script
*   PySide      -- tested with 1.1.0, package python3-pyside in Ubuntu
*   xsel        -- for using X11 clipboard functionality

### Features

*   save input to file in temp folder and run it
*   output result in output box
*   highlight stderr output red
*   put return code in the return code field

