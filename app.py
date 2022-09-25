from tkinter import ttk, PhotoImage
from ttkthemes import ThemedTk
from data.data import RepositorioRendaFixa, RepositorioRendaVariavel


class PyInvest:

    def __init__(self):
        
        # MASTER
        self.master = ThemedTk(theme='black')
        self.master.title('PyInvets')
        self.master.configure(background='#444444')
        w = int(self.master.winfo_screenwidth() / 2 - 640)
        h = int(self.master.winfo_screenheight() / 2 - 320)
        self.master.geometry(f'1280x640+{w}+{h}')
        self.master.iconbitmap(default='images/logo.ico')

        # IMAGES
        self.img_purshase = PhotoImage(file='images/btn_purchase.png')

        # FRAME FOR BUTTONS
        self.frame_b = ttk.Frame(self.master,
                                relief='ridge',
                                borderwidth=2,
                                )
        self.frame_b.grid(row=0, column=0, padx=10, pady=10)

        # FRAME FOR REPORT
        self.frame_report = ttk.Frame(self.master,
                                     relief='ridge',
                                     borderwidth=2,
                                     )
        self.frame_report.grid(row=0, column=1)

        # BUTTONS
        self.s = ttk.Style()
        self.s.configure('P.TButton', relief='flat', background='red')
        self.s.map('P.TButton',
            foreground=[('!active', 'black'),('pressed', 'red'), ('active', 'white')],
            background=[ ('!active','#444444'),('pressed', '#444444'), ('active', '#444444')],
            highlightthickness=[('pressed', -10)],
            relief=[ ('!active','flat'),('pressed', 'flat'), ('active', 'flat')]
            )
        self.button_register = ttk.Button(self.frame_b,
                                         text='CADASTRAR',
                                         command=None)
        self.button_register.grid(row=0, column=0, padx=10, pady=10)

        self.button_purchase = ttk.Button(self.frame_b,
                                         image=self.img_purshase,
                                         style='P.TButton',
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

        # LABELS FOR REPORTS
        self.label_actions = ttk.Label(self.frame_report,
                                       text=f'Total investido em Ações: R$ {self.report_actions()}',
                                       font='arial 20',
                                       foreground='white',
                                       )
        self.label_actions.grid(row=0, column=0, padx=5, pady=5)

        self.label_fii = ttk.Label(self.frame_report,
                                   text=f'Total investido em FIIs: R$ {self.report_fiis()}',
                                   font='arial 20',
                                   foreground='white',
                                   )
        self.label_fii.grid(row=1, column=0, padx=5, pady=5)

        self.label_direct_treasure = ttk.Label(self.frame_report,
                                              text=f'Total investido no Tesouro Direto: R$ {self.report_direct_treasure()}',
                                              font='arial, 20',
                                              foreground='white',
                                              )
        self.label_direct_treasure.grid(row=2, column=0, padx=5, pady=5)

        self.label_fixed_income = ttk.Label(self.frame_report,
                                            text=f'Total investido em Renda Fixa: R$ {self.report_fixed_income()}',
                                            font='arial, 20',
                                            foreground='white',
                                            )
        self.label_fixed_income.grid(row=3, column=0, padx=5, pady=5)

        self.label_emergency_reserve = ttk.Label(self.frame_report,
                                                text=f'Total na Reserva de Emergência: R$ {self.report_emergency_reserv()}',
                                                font='arial 20',
                                                foreground='white',
                                                )
        self.label_emergency_reserve.grid(row=4, column=0, padx=5, pady=5)

        self.label_total_invest = ttk.Label(self.frame_report,
                                            text=f'Total investido: R$ {self.report_total_invested()}',
                                            font='arial 24 bold',
                                            foreground='darkgreen',
                                            )
        self.label_total_invest.grid(row=5, column=0)


        # INFINITE LOOP
        self.master.mainloop()
    
    # FUNCTIONS
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


PyInvest()
