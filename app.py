from tkinter import *
from tkinter import ttk


master = Tk()

dados = StringVar()

dados.set('Meus Dados')

entry = ttk.Entry(master,
                  textvariable=dados,
                  state='readonly',
                  ).grid()

master.mainloop()