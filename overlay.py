from tkinter import *
from tkinter import messagebox
import keyboard
import threading
import os

root=Tk()

######## Admin Check ############
# (need admin for global listener)

import ctypes

def is_admin():
    try:
        # Windows
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        # Unix/Linux/macOS
        return os.geteuid() == 0

# Show error popup and exit if not admin/root
if not is_admin():
    root.withdraw()  # Hide the main window
    messagebox.showerror("Permission Denied", "This script must be run as Administrator (Windows) or with sudo (Linux/macOS).")
    exit(1)

############ Setup ###############

root.title("NIV Overlay")

x="0"
y="0"

root.geometry(f'250x150+{x}+{y}')
# to remove the titlebar 
root.overrideredirect(True)

# to make the window transparent  
root.attributes("-transparentcolor","red")
# set bg to red in order to make it transparent
root.config(bg="red")

########## Create Widgets ############

#l=Label(root,text="HI this is an overlay",fg="white",font=(60),bg="red")
#l.pack()

b=Button(root,text="Exit",command=lambda:exit(0))
b.pack()


######### Create Callbacks ###########

def on_page_change(n):
    print(n)

def setup_hotkeys():
    # Flip pages
    keyboard.add_hotkey(".", lambda:on_page_change(1))
    keyboard.add_hotkey(",", lambda:on_page_change(-1))

threading.Thread(target=setup_hotkeys, daemon=True).start()

#######################################

# make window to be always on top 
root.wm_attributes("-topmost", 1) 
root.mainloop()
