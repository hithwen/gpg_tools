#!/usr/bin/env bash
pyinstaller cli.py --name gpgclip --onefile  --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'
