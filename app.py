from tkinter import Tk, ttk
from ttkthemes import ThemedTk

master = ThemedTk(theme='blue')

s = ttk.Style('TButton',
             )

button = ttk.Button(master,
                    text='Teste',
                    borderwidth=0,
                    )
button.pack()


master.mainloop()
