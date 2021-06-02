
from matplotlib.colors import Normalize
import pandas_datareader
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from yahoo_fin.stock_info import *
import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import os
import time
from mpl_finance import candlestick_ohlc

isMonitoring = False

os.chdir('C:/Users/parke/Documents/GitHub/StonkStuff')

#SETTING UP ROOT WINDOW~~~~~~~~
root = tk.Tk()
root.title('~Stonk Stuff v0.2')
root.geometry('1000x400')
root.configure()
root.iconbitmap('StonkStuff/rocket2.ico')
root.resizable(False, False)
root.attributes('-topmost', True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#IMAGES AND FONTS~~~~~~~~~~~~~~
space_img = ImageTk.PhotoImage(Image.open("StonkStuff/space_2.png"))
space_label = Label(image = space_img)
space_label.place(x=-2, y=-2)

moon_img = ImageTk.PhotoImage(Image.open("StonkStuff/moon.png"))
moon_label = Label(image=moon_img, borderwidth=0)
moon_label.place(x=250)

doge_img = ImageTk.PhotoImage(Image.open("StonkStuff/doge3.png"))
doge_label = Label(image = doge_img, background='#17211E')
doge_label.place(y = 220)

courier_new = font.Font(family='Courier New', size=20)
font2 = font.Font(family='Comic Sans MS', size=8)
font3 = font.Font(family='Comic Sans MS', size=20)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#METHODS~~~~~~~~~~~~~~~~~~~~~~~
def enterStock(event=None):
    global isMonitoring
    global priceLabel
    global tickerLabel

    isMonitoring = True
    ticker = entry.get()
    livePrice = get_live_price(ticker.upper())
    priceLabel = Label(root, text=livePrice, bg='#C09F52', foreground='#00FF21', font=courier_new, borderwidth=3, relief="ridge", width=20)
    priceLabel.place(x=45, y=150)
    tickerLabel = Label(root, text=ticker.upper(), bg='#C09F52', foreground='black', font=courier_new, borderwidth=3, relief='ridge', width=9)
    tickerLabel.place(relx=.125, y=110)
    while isMonitoring:
        priceLabel.configure(text=get_live_price(ticker.upper()))
        root.update()



def cancelProcess():
    global isMonitoring
    isMonitoring = False
    tickerLabel.destroy()
    priceLabel.destroy()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TEXT ENTRY FIELD~~~~~~~~~~~~~~
entry = Entry(root, width=25, borderwidth=1)
entry.place(x=125, y=5)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#BUTTONS~~~~~~~~~~~~~~~~~~~~~~~
button = Button(root, text="Much Start", command=enterStock, width=21, borderwidth=1, background='green', relief='ridge', font=font2)
button.place(x=125, y=35)

cancelButton = Button(root, text="Such Stop", command=cancelProcess, width=21, borderwidth=1, background='maroon', relief='ridge', font=font2)
cancelButton.place(x=125, y=65)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#GRAPH~~~~~~~~~~~~~~~~~~~~~~~~~
start = dt.datetime(2021, 3, 1)
end = dt.datetime.now()
data = pandas_datareader.DataReader('DOGE-USD', 'yahoo', start, end)
data = data[['Open', 'High', 'Low', 'Close']]
data.reset_index(inplace=True)
data['Date'] = data['Date'].map(mdates.date2num)

f = Figure(figsize=(1, 1), dpi=65)
a = f.add_subplot(111)
a.grid(True)
a.set_axisbelow(True)
a.set_title('DOGE Price', color='white')
a.set_facecolor('#17211E')
a.figure.set_facecolor('#17211E')
a.tick_params(axis='x', colors='white')
a.tick_params(axis='y', colors='white')
myFmt = DateFormatter("%m/%d")
a.xaxis.set_major_formatter(myFmt)
#a.xaxis_date()
candlestick_ohlc(a, data.values, width=.25, colorup='#00ff00')
canvas = FigureCanvasTkAgg(f, root)
canvas.draw()
canvas.get_tk_widget().place(x=400, y=0, width=600, height=400)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


root.bind('<Return>', enterStock)
root.mainloop()