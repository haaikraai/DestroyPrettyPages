import os
import pyquery
import lxml.html
import requests
from bs4 import BeautifulSoup, Tag
import time
import tkinter
import webview
from DestroyPrettyPage import DestroyPrettyPage as dpp

def tkinter_stuff():
    root = tkinter.Tk()
    root.geometry('800x600')
    root.grid_size(4, 1)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    print(screen_width)
    options_frame = tkinter.Frame(root, width=400, height=600)
    label = tkinter.Label(options_frame, text='WIDTH:').grid(row=0, column=0)
    label = tkinter.Label(options_frame, text=str(screen_width)).grid(row=1, column=0)
    label = tkinter.Label(options_frame, text='HEIGHT:').grid(row=2, column=0)
    label = tkinter.Label(options_frame, text=str(screen_height)).grid(row=3, column=0)

    options_frame.place(x = 100, y=100)
    preview_frame = tkinter.Frame(root, width=400, height=600, container=True, bg='darkgray')
    preview_frame.place(x = 500, y=100)

    # print(root.attributes('-fullscreen', 1))
    root.attributes('-topmost',1)
    print(root.configure().keys())
    '''
    {'bd': ('bd', '-borderwidth'), 'borderwidth': ('borderwidth', 'borderWidth', 'BorderWidth', <string object: '0'>, 0), 'class': ('class', 'class', 'Class', 'Toplevel', 'Tk'), 'menu': ('menu', 'menu', 'Menu', '', ''), 'relief': ('relief', 'relief', 'Relief', <string object: 'flat'>, 'flat'), 'screen': ('screen', 'screen', 'Screen', '', ''), 'use': ('use', 'use', 'Use', '', ''), 'background': ('background', 'background', 'Background', <string object: 'SystemButtonFace'>, 'SystemButtonFace'), 'bg': ('bg', '-background'), 'colormap': ('colormap', 'colormap', 'Colormap', '', ''), 'container': ('container', 'container', 'Container', 0, 0), 'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 'height': ('height', 'height', 'Height', <string object: '0'>, 0), 'highlightbackground': ('highlightbackground', 'highlightBackground', 'HighlightBackground', <string object: 'SystemButtonFace'>, 'SystemButtonFace'), 'highlightcolor': ('highlightcolor', 'highlightColor', 'HighlightColor', <string object: 'SystemWindowFrame'>, 'SystemWindowFrame'), 'highlightthickness': ('highlightthickness', 'highlightThickness', 'HighlightThickness', <string object: '0'>, 0), 'padx': ('padx', 'padX', 'Pad', <string object: '0'>, <string object: '0'>), 'pady': ('pady', 'padY', 'Pad', <string object: '0'>, <string object: '0'>), 'takefocus': ('takefocus', 'takeFocus', 'TakeFocus', '0', '0'), 'visual': ('visual', 'visual', 'Visual', '', ''), 'width': ('width', 'width', 'Width', <string object: '0'>, 0)}
    '''

    # root.attributes('-disabled', 1)
    # root.attributes('-fullscreen', 1)

    root.mainloop()

    # webview.create_window('Attached', 'https://www.google.com')


def soup_stuff():
    # d = pyquery.PyQuery('https://www.javatpoint.com/android-tutorial')
    html = ''
    with open('test.html', 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')


    # soup = BeautifulSoup(requests.get('https://www.javatpoint.com/android-tutorial').text, 'html.parser')

    navcontainer = soup.select('.container')
    tests = navcontainer[-1](True)

    for link in tests:
        link: Tag = link
        print(link)
        print('Attributes...')
        time.sleep(2)
        print(link.attrs)
    
    return link

def destroy_stuff():
    # dps = dpp('https://www.javatpoint.com/android-tutorial')
    dps = dpp('test.html')
    return dps


last = destroy_stuff()

m = last.soup.find('h1')
tit = last.soup.find('h2')
span = last.soup.find('span')
print(m)
print(tit)
print(span)

ne = tit.append(span)