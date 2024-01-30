import os
import sys
import pyshark                          # Used to capture packets from pcap
from user_agents import parse           # Getting device type from useragent
from tkinter import *                   # GUI
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.font as tkFont

heading = 'Device Type Detection'
root = Tk(className=heading.title())
fontStyle = tkFont.Font(family="Lucida Grande", size=10)
fontStyle1 = tkFont.Font(family="Lucida Grande", size=25, weight="bold")
root.geometry("2000x800")
root.title(heading)


image = Image.open("bg.jpg")            
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)
#label.place(x=0, y=0, relheight=1, relwidth=1)

def isMobileDevice(useragent):
    user_agent = parse(useragent)
    if user_agent.is_mobile:
        return True
    else:
        return False

def isTabletDevice(useragent):
    user_agent = parse(useragent)
    if user_agent.is_tablet:
        return True
    else:
        return False

def isPC(useragent):
    user_agent = parse(useragent)
    if user_agent.is_pc:
        return True
    else:
        return False

def getUserAgent():
    root.filename = filedialog.askopenfilename(
        initialdir="/", title="Select file")

    if root.filename == '':
        print("No file selected")
        sys.exit()
    else:
        useragents = []
        cap = pyshark.FileCapture(
            root.filename, display_filter='frame contains "GET"')
        for packet in cap:
            print(packet['http'].user_agent)
            useragents.append(packet['http'].user_agent)
        i = 0
        for useragent in useragents:
            i = i+1
            if isMobileDevice(useragent):
                myLabel = Label(
                    root, text="Device Type : Mobile 📱", font=fontStyle1, fg="white", bg="#042592")
                myLabel.pack()
            elif isTabletDevice(useragent):
                myLabel = Label(
                    root, text="Device Type : Tablet 📱", font=fontStyle1, fg="white", bg="#042592")
                myLabel.pack()
            elif isPC(useragent):
                myLabel = Label(
                    root, text="Device Type : Desktop 🖥️", font=fontStyle1, fg="white", bg="#042592")
                myLabel.pack()
            else:
                myLabel = Label(
                    root, text="Device Type : Unknown❓", font=fontStyle1, fg="white", bg="#042592")
                myLabel.pack()

            myLabel = Label(root, text="Packet"+str(i) +
                            ": " + useragent+"\n", font=fontStyle, fg="white", bg="#042592")

            myLabel.pack()

        cap.close()


fileInputBtn = Button(root, text="Choose file", font=tkFont.Font(family="Lucida Grande", size=15),
                      command=getUserAgent).pack(
    side=TOP, pady=20, padx=20)

root.mainloop()