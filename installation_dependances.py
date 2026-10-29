import os
import sys

if '-unix' in sys.argv:
    os.system("python3 -m pip install ursina")
    os.system("python3 -m pip install psutil")
    os.system("python3 -m pip install customtkinter")
    os.system("python3 -m pip install CTkListbox")
else:
    os.system("py -m pip install ursina")
    os.system("py -m pip install psutil")
    os.system("py -m pip install customtkinter")
    os.system("py -m pip install CTkListbox")
