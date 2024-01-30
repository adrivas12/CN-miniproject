import os
import sys
import pyshark
from user_agents import parse
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.font as tkFont

def selectFileAndExtractPackets():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    if root.filename == '':
        print("No file selected")
        sys.exit()
    else:
        useragents = []
        cap = pyshark.FileCapture(root.filename, display_filter='frame contains "GET"')
        for packet in cap:
            useragents.append(packet['http'].user_agent)
        cap.close()
    return useragents

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

def detectDevices(useragents):
    detected_devices = []
    for useragent in useragents:
        if isMobileDevice(useragent):
            detected_devices.append("Device Type : Mobile 📱")
        elif isTabletDevice(useragent):
            detected_devices.append("Device Type : Tablet 📱")
        elif isPC(useragent):
            detected_devices.append("Device Type : Desktop 🖥️")
        else:
            detected_devices.append("Device Type : Unknown❓")
    return detected_devices

def setupGUI(detected_devices):
    root = Tk(className='Device Type Detection')
    fontStyle = tkFont.Font(family="Lucida Grande", size=10)
    fontStyle1 = tkFont.Font(family="Lucida Grande", size=25, weight="bold")
    root.geometry("2000x800")
    
    image = Image.open("bg.jpg")
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.place(x=1, y=1, relheight=3.5, relwidth=3.5)

    i = 0
    for device_type in detected_devices:
        i += 1
        myLabel = Label(root, text=f"Packet {i}: {device_type}\n", font=fontStyle, fg="white", bg="#042592")
        myLabel.pack()

    fileInputBtn = Button(root, text="Choose file", font=tkFont.Font(family="Lucida Grande", size=15),
                          command=selectFileAndExtractPackets)
    fileInputBtn.pack(side=TOP, pady=20, padx=20)

    root.mainloop()

# Main code
root = Tk(className='Device Type Detection')
useragents = selectFileAndExtractPackets()
detected_devices = detectDevices(useragents)
setupGUI(detected_devices)
root.mainloop()