from tkinter import ttk, Toplevel
from ttkthemes import ThemedTk
from data.data import RepositorioRendaFixa, RepositorioRendaVariavel


class PyInvest:

    def __init__(self):
        
        # MASTER
        self.master = ThemedTk(theme='black')
        self.master.title('PyInvets')
        self.master.configure(background='#000000')
        self.set_size_window(self.master, 1016, 490)
        self.master.iconbitmap(default='images/logo.ico')

        # BUTTONS OF MENU
        self.frame_buttons = ButtonMenu(self.master)

        # FRAME FOR REPORTS
        self.frame_report = FrameReport(self.master)   

        # INFINITE LOOP
        self.master.mainloop()
    
    # FUNCTIONS
    def set_size_window(self, window, width, height):
        w = int((window.winfo_screenwidth() / 2) - (width/2))
        h = int((window.winfo_screenheight() / 2) - (height/2))
        window.geometry(f'{width}x{height}+{w}+{h}')

class ButtonMenu(ttk.Frame):
    
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # FRAME FOR BUTTONS
        self.frame_b = ttk.Frame(self.master,
                                relief='ridge',
                                borderwidth=2,
                                )
        self.frame_b.grid(row=0, column=0, padx=10, pady=10, sticky=('n', 'e', 's', 'w'))

        # BUTTONS
        self.s = ttk.Style()
        self.s.configure('TButton',
                        width=23,
                        padding=10,
                        anchor='center',
                        font='arial 20',
                        )
        self.s.map('TButton',
                    background=[('!active', '#009E2D'),
                                ('pressed', '#9BF0B7'), 
                                ('active', '#10EB4E'), 
                                ],
                    foreground=[('pressed', '#575757')]
                                )

        self.button_register = ttk.Button(self.frame_b,
                                         text='CADASTRAR',
                                         command= lambda :TopLevelRegister(self.master),
                                         )
        self.button_register.grid(row=0, column=0, padx=10, pady=10)

        self.button_purchase = ttk.Button(self.frame_b,
                                         text='COMPRAR',
                                         command=None)
        self.button_purchase.grid(row=1, column=0, padx=10, pady=10)

        self.button_sell = ttk.Button(self.frame_b,
                                     text='VENDER',
                                     command=None,
                                     )
        self.button_sell.grid(row=2, column=0, padx=10, pady=10)

        self.button_m_value = ttk.Button(self.frame_b,
                                        text='ACERTAR VALOR',
                                        command=None,
                                        )
        self.button_m_value.grid(row=3, column=0, padx=10, pady=10)

        self.button_m_amount = ttk.Button(self.frame_b,
                                         text='ACERTAR QUANTIDADE',
                                         command=None,
                                         )
        self.button_m_amount.grid(row=4, column=0, padx=10, pady=10)

        self.button_delete = ttk.Button(self.frame_b,
                                        text='EXCLUIR',
                                        command=None,
                                        )
        self.button_delete.grid(row=5, column=0, padx=10, pady=10)

class FrameReport(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
    
        # FRAME FOR REPORT
        self.frame_report = ttk.Frame(self.master,
                                     relief='ridge',
                                     borderwidth=2,
                                     )
        self.frame_report.grid(row=0, column=1, padx=5, pady=10, sticky=('n', 'e', 's', 'w'))

        # LABELS FOR REPORTS
        self.s = ttk.Style()
        self.s.configure('L.TLabel', font='arial, 20', foreground='white')

        self.label_actions = ttk.Label(self.frame_report,
                                       text=f'Total investido em Ações: R$ {self.report_actions()}',
                                       style='L.TLabel',
                                       )
        self.label_actions.grid(row=0, column=0, padx=5, pady=5)

        self.label_fii = ttk.Label(self.frame_report,
                                   text=f'Total investido em FIIs: R$ {self.report_fiis()}',
                                   style='L.TLabel',
                                   )
        self.label_fii.grid(row=1, column=0, padx=5, pady=5)

        self.label_direct_treasure = ttk.Label(self.frame_report,
                                              text=f'Total investido no Tesouro Direto: R$ {self.report_direct_treasure()}',
                                              style='L.TLabel',
                                              )
        self.label_direct_treasure.grid(row=2, column=0, padx=5, pady=5)

        self.label_fixed_income = ttk.Label(self.frame_report,
                                            text=f'Total investido em Renda Fixa: R$ {self.report_fixed_income()}',
                                            style='L.TLabel',
                                            )
        self.label_fixed_income.grid(row=3, column=0, padx=5, pady=5)

        self.label_emergency_reserve = ttk.Label(self.frame_report,
                                                text=f'Total na Reserva de Emergência: R$ {self.report_emergency_reserv()}',
                                                style='L.TLabel',
                                                )
        self.label_emergency_reserve.grid(row=4, column=0, padx=5, pady=5)

        self.label_total_invest = ttk.Label(self.frame_report,
                                            text=f'Total investido: R$ {self.report_total_invested()}',
                                            font='arial 24 bold',
                                            foreground='#009E2D',
                                            )
        self.label_total_invest.grid(row=5, column=0)
    
    def report_actions(self):
        rep = RepositorioRendaVariavel()
        tot = rep.relatorio_acoes()
        return f'{tot:.2f}'

    def report_fiis(self):
        rep = RepositorioRendaVariavel()
        tot = rep.relatorio_fiis()
        print(tot)
        return f'{tot:.2f}'

    def report_emergency_reserv(self):
        rep = RepositorioRendaFixa()
        tot = rep.relatorio_res_emerg()
        return f'{tot:.2f}'
    
    def report_direct_treasure(self):
        rep = RepositorioRendaFixa()
        tot = rep.relatorio_tesouro_direto()
        return f'{tot:.2f}'

    def report_fixed_income(self):
        rep = RepositorioRendaFixa()
        tot = rep.relatorio_renda_fixa()
        return f'{tot:.2f}'
    
    def report_total_invested(self):
        rv = RepositorioRendaVariavel()
        rf = RepositorioRendaFixa()

        actions = rv.relatorio_acoes()
        fiis = rv.relatorio_fiis()
        fixed_income = rf.relatorio_renda_fixa()
        direct_treasure = rf.relatorio_tesouro_direto()
        emergency_reserve = rf.relatorio_res_emerg()
        list_of_invest = [actions, fiis, fixed_income, direct_treasure, emergency_reserve]

        tot = sum([value for value in list_of_invest])

        return f'{tot:.2f}'

class TopLevelRegister:

    def __init__(self, master):
        self.top_level = Toplevel(master)
        self.top_level.title('Cadastrar novo ativo')
        self.top_level.iconbitmap(default='images/logo.ico')
        self.top_level.configure(background='#000000')
        self.set_size_window(self.top_level, 400, 400)

        self.button_fixed_income = ttk.Button(self.top_level,
                                              text='Renda Fixa',
                                              command=None)
        self.button_fixed_income.place(x=14, y=120)

        self.button_variable_income = ttk.Button(self.top_level,
                                                 text='Renda Variável',
                                                 command=None,
                                                 )
        self.button_variable_income.place(x=14, y=190)

    # FUNCTIONS
    def set_size_window(self, window, width, height):
        w = int((window.winfo_screenwidth() / 2) - (width/2))
        h = int((window.winfo_screenheight() / 2) - (height/2))
        window.geometry(f'{width}x{height}+{w}+{h}')


PyInvest()
