from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
import keyboard
import threading
import os
import math

root=Tk()

# Configure
afont = tkfont.Font(family="Helvetica", size=20)

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

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x="0"
y="0"

root.geometry(f'{screen_width}x{screen_height}+{x}+{y}')
# to remove the titlebar 
root.overrideredirect(True)

# to make the window transparent  
root.attributes("-transparentcolor","black")
# set bg to black in order to make it transparent
root.config(bg="black")

########## Create Widgets ############

def calculate_lines(text, width):
    """Calculate the number of lines for the given text and width using a temporary Text widget."""
    temp_text = Text(root, wrap='word', height=0, font=afont)
    temp_text.insert('1.0', text)
    temp_text.place_configure(width=width, height=1000)
    #print(temp_text.index('end-1c'))
    line_count = math.ceil(float(temp_text.index('end-1c')))  # Get the line count

    temp_text.destroy()
    return line_count

l = Canvas(root, width=screen_width//2, height=screen_height, bg='black',
           highlightthickness=0,  # removes the border
            bd=0)
l.place_configure(x=screen_width//4, y=0)

def update_label(text):
    #text = l.cget("text")
    line_count = calculate_lines(text, screen_width//2)
    
    line_height = afont.metrics('linespace')
    text_height = line_count * line_height
    
    # Calculate the y-position so that the bottom of the text is 1/6 from the screen's bottom
    y_position = screen_height - (screen_height // 6) - text_height
    
    # Update the position of the text
    l.delete("all")

    # shadow
    i = 0
    shadow_dist = 2
    for xo in [-shadow_dist, 0, shadow_dist]:
        for yo in [-shadow_dist, 0, shadow_dist]:
            if xo == 0 and yo == 0:
                continue
            l.create_text(shadow_dist + xo, y_position + yo, anchor='w', text=text, width=screen_width//2 - shadow_dist, font=afont, fill='#2b2b2b')
            i += 1
    
    l.create_text(shadow_dist, y_position, anchor='w', text=text, width=screen_width//2 - shadow_dist, font=afont, fill='white')

update_label("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")

b=Button(root,text="Exit",command=lambda:exit(0),fg='#2b2b2b')
b.place_configure(x=screen_width-100, y=screen_height-100)


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
