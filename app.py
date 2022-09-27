from tkinter import ttk, Toplevel
from tkinter.messagebox import showerror, showinfo
from ttkthemes import ThemedTk
from ativo_factory import AtivoFactory
from data.data import RepositorioRendaFixa, RepositorioRendaVariavel
from time import sleep
from data.data import RepositorioRendaFixa, RepositorioRendaVariavel
from data.exceptions import AtivoJaCadastradoError


class PyInvest:
    def __init__(self):
        
        # MASTER
        self.master = ThemedTk(theme='black')
        self.master.title('PyInvets')
        self.master.configure(background='#000000')
        self.general_functions = GeneralFunctions()
        self.general_functions.set_size_window(self.master, 1016, 490)
        self.master.iconbitmap(default='images/logo.ico')

        # BUTTONS OF MENU
        self.frame_buttons = ButtonMenu(self.master)

        # FRAME FOR REPORTS
        self.frame_report = FrameReport(self.master)   

        # INFINITE LOOP
        self.master.mainloop()


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
        self.general_functions = GeneralFunctions()
        self.general_functions.set_size_window(self.top_level, 400, 400)

        self.button_fixed_income = ttk.Button(self.top_level,
                                              text='Renda Fixa',
                                              command=lambda: self.open_toplevel_fixed_income(master),
                                              )
        self.button_fixed_income.place(x=14, y=120)

        self.button_variable_income = ttk.Button(self.top_level,
                                                 text='Renda Variável',
                                                 command=lambda: self.open_toplevel_variable_income(master),
                                                 )
        self.button_variable_income.place(x=14, y=190)
    
    # FUNCTIONS
    def open_toplevel_variable_income(self, master):
        self.top_level.destroy()
        sleep(1)
        top_level_variable_income = TLRegVariableIncome(master,
                                                    'Cadastro Renda Variável',
                                                    "images/logo.ico",
                                                    '#000000',
                                                    580,
                                                    400,)
    
    def open_toplevel_fixed_income(self, master):
        self.top_level.destroy()
        sleep(1)
        top_level_fixed_income = TLRegFixedleIncome(master,
                                                        'Cadastro Renda Fixa',
                                                        "images/logo.ico",
                                                        '#000000',
                                                        600,
                                                        400,
                                                        )

class TLRegVariableIncome:
    def __init__(self, master, title, logo: tuple, color, width, height):
        self.top_level = Toplevel(master)
        self.top_level.title(title)
        self.top_level.iconbitmap(default=logo)
        self.top_level.configure(background=color)
        general_functions = GeneralFunctions()
        general_functions.set_size_window(self.top_level, width, height)

        # VARIABLES
        self.repository = AtivoFactory()
        self.check_action = False
        self.check_fii = False

        # STYLES
        s = ttk.Style()
        s.configure('RV.TRadiobutton',
                    background='#000000',
                    foreground='white',
                    font='arial 20',
                    )
                    
        s.configure('RV.TFrame',
                    background='#000000',
                    )
        
        s.configure('RV.TLabel',
                    background='#000000',
                    foreground='white',
                    font='arila 20',
                    padding=10,
                    )

        # NAME
        label_name = ttk.Label(self.top_level,
                        text='Nome:',
                        style='RV.TLabel'
                        )
        label_name.grid(row=0, column=0)

        self.entry_name = ttk.Entry(self.top_level,
                                width=30,
                                font='arial, 20',
                                )
        self.entry_name.grid(row=0, column=1)

        # CODE
        label_code = ttk.Label(self.top_level,
                                text='Código',
                                style='RV.TLabel'
                                )
        label_code.grid(row=1, column=0)

        self.entry_code = ttk.Entry(self.top_level,
                                width=30,
                                font='arial 20',
                                )
        self.entry_code.grid(row=1, column=1)

        # OPTIONS
        frame = ttk.Frame(self.top_level, style='RV.TFrame')
        frame.grid(row=2, column=0, columnspan=2)

        action = ttk.Radiobutton(frame,
                                text='Ações',
                                value=0,
                                style='RV.TRadiobutton',
                                padding=10,
                                command=self.validate_action,
                                )
        action.grid(row=0, column=0)

        fii = ttk.Radiobutton(frame,
                              text='FIIs',
                              value=1,
                              style='RV.TRadiobutton',
                              padding=10,
                              command=self.validate_fii,
                              )
        fii.grid(row=1, column=0)

        # BUTTONS
        frame_options = ttk.Frame(self.top_level, style='RV.TFrame')
        frame_options.grid(row=3, column=0, columnspan=2)
        button_register = ttk.Button(frame_options,
                                    text='CADASTRAR',
                                    command=self.register,
                                    )
        button_register.grid(row=0, column=0, pady=10)

        button_cancel = ttk.Button(frame_options,
                                   text='CANCELAR',
                                   command=self.quit,
                                   )
        button_cancel.grid(row=1, column=0, pady=10)
    
    def validate_action(self):
        self.check_action = True
        self.check_fii = False

    def validate_fii(self):
        self.check_action = False
        self.check_fii = True

    def register(self):
        if self.check_action:
            try:
                name = self.entry_name.get().title()
                code = self.entry_code.get().upper()

                if len(name) == 0 or len(code) == 0:
                    showerror(message='Preencha todos os dados')
                elif len(code) < 5:
                    showerror(message='O código precisa ter pelo menos 5 caracteres')
                else:
                    self.repository.criar_acao(name, code)
                    showinfo(message='Ativo cadastrado com sucesso.')
            except AtivoJaCadastradoError:
                showerror(message='Ativo já cadastrado no banco de dados')
            
        if self.check_fii:
            try:
                name = self.entry_name.get().title()
                code = self.entry_code.get().upper()

                if len(name) == 0 or len(code) == 0:
                    showerror(message='Preencha todos os dados')
                elif len(code) < 5:
                    showerror(message='O código precisa ter pelo menos 5 caracteres')
                else:
                    self.repository.criar_fii(name, code)
                    showinfo(message='Ativo cadastrado com sucesso.')
            except AtivoJaCadastradoError:
                showerror(message='Ativo já cadastrado no banco de dados')
        
    def quit(self):
        self.top_level.destroy()

class TLRegFixedleIncome:
    def __init__(self, master, title, logo: tuple, color, width, height):
        self.top_level = Toplevel(master)
        self.top_level.title(title)
        self.top_level.iconbitmap(default=logo)
        self.top_level.configure(background=color)
        general_functions = GeneralFunctions()
        general_functions.set_size_window(self.top_level, width, height)


class GeneralFunctions:
    @staticmethod
    def set_size_window(window, width, height):
        w = int((window.winfo_screenwidth() / 2) - (width/2))
        h = int((window.winfo_screenheight() / 2) - (height/2))
        window.geometry(f'{width}x{height}+{w}+{h}')
    

# ALTERAR A LOGO PARA SER UMA VARIÁVEL DE USO GLOBAL
# SE PRECISAR ALTERAR, ALTERA APENAS UMA VEZ.

PyInvest()
