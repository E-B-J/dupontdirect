# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 19:53:04 2023

@author: ebjam
"""

import requests
import xml.etree.ElementTree as ET
import tkinter as tk

def get_next_busses(stopId):
    req_xml = "https://retro.umoiq.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=" + str(stopId)
    joe = ET.fromstring(requests.get(req_xml).text)
    predictions = []
    for prediction in joe.findall(".//prediction"):
        minutes = prediction.get("minutes")
        branch = prediction.get("branch")
        predictions.append({"minutes": minutes, "branch": branch})
    return(predictions)

def sorted_times(predictions):
    times = []
    for prediction in predictions:
        times.append(prediction["minutes"])
    times.sort()
    return(times)

def get_line_times():
    fourtyseven = {'north': sorted_times(get_next_busses(4401))[:2], 'south': sorted_times(get_next_busses(4402))[:2]}
    twentysix = {'east': sorted_times(get_next_busses(1015))[:2], 'west':sorted_times(get_next_busses(1016))[:2]}
    return({47: fourtyseven, 26: twentysix})

dicto = get_line_times()

root = tk.Tk()
root.geometry('1709x1135')
root.title('Dictionary Display')

# Set up background image
bg_image = tk.PhotoImage(file='C:/Users/ebjam/bg2.png')
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create labels for each direction
north_label = tk.Label(root, text=f"{', '.join(dicto[47]['north'])}", bg="white", font=('Arial', 72, 'italic', 'bold'), fg = 'maroon')
south_label = tk.Label(root, text=f"{', '.join(dicto[47]['south'])}", bg="white", font=('Arial', 72, 'italic', 'bold'), fg = 'maroon')
east_label = tk.Label(root, text=f"{', '.join(dicto[26]['east'])}", bg="white", font=('Arial', 72, 'italic', 'bold'), fg = 'dark blue')
west_label = tk.Label(root, text=f"{', '.join(dicto[26]['west'])}", bg="white", font=('Arial', 72, 'italic', 'bold'), fg = 'dark blue')

# Place labels in correct positions
north_label.place(relx=0.73, rely=0.037)
south_label.place(relx=0.73, rely=0.29)
east_label.place(relx=0.15, rely=0.57)
west_label.place(relx=0.15, rely=0.84)

def update_dicto():
    dicto = get_line_times()
    north_label = tk.Label(root, text=f"{', '.join(dicto[47]['north'])}", bg="white", font=('Arial', 50, 'italic', 'bold'), fg = 'maroon')
    south_label = tk.Label(root, text=f"{', '.join(dicto[47]['south'])}", bg="white", font=('Arial', 50, 'italic', 'bold'), fg = 'maroon')
    east_label = tk.Label(root, text=f"{', '.join(dicto[26]['east'])}", bg="white", font=('Arial', 50, 'italic', 'bold'), fg = 'dark blue')
    west_label = tk.Label(root, text=f"{', '.join(dicto[26]['west'])}", bg="white", font=('Arial', 50, 'italic', 'bold'), fg = 'dark blue')

    # Place labels in correct positions
    north_label.place(relx=0.73, rely=0.037)
    south_label.place(relx=0.73, rely=0.29)
    east_label.place(relx=0.15, rely=0.57)
    west_label.place(relx=0.15, rely=0.84)
    
# Schedule the first update in 1 minute
root.after(60000, update_dicto)

root.mainloop()