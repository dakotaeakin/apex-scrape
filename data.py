import os
import tkinter as tk
import hashlib
import pickle
from stor import *


# salt = os.urandom(32)
#
# root = tk.Tk()
#
# canvas1 = tk.Canvas(root, width=400, height=300)
# canvas1.pack()
#
# entry1 = tk.Entry(root)
# canvas1.create_window(200, 140, window=entry1)
#
#
# def getSquareRoot():
#     password = entry1
#     key = hashlib.pbkdf2_hmac(
#         'sha256', f'{password}'.encode('UTF-8'), salt, 100000
#     )
#     storage = salt + key
#     print(storage)
#     file = 'data.pickle'
#     outfile = open(file, 'wb')
#     pickle.dump(storage, outfile)
#     outfile.close()
#
#
# button1 = tk.Button(text='Get the Square Root', command=getSquareRoot)
# canvas1.create_window(200, 180, window=button1)
#
# root.mainloop()

password = password()

print(password)
