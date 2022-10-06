from msilib.schema import ComboBox
from time import sleep
from tkinter import Listbox, Toplevel, font, ttk, StringVar
from tkinter.messagebox import showerror, showinfo
from ttkthemes import ThemedTk
from ativo_factory import AtivoFactory
from data.data import RepositorioRendaFixa, RepositorioRendaVariavel
from data.exceptions import AtivoJaCadastradoError, FaltamDadosErros


class PyInvest:
    def __init__(self):
                        
        # MASTER
        self.master = ThemedTk(theme='black')
        self.master.title('PyInvest')
        self.master.configure(background='#000000')
        self.general_functions = GeneralFunctions()
        self.general_functions.set_size_window(self.master, 1016, 490)

        # BUTTONS OF MENU
        self.frame_buttons = ButtonMenu(self.master)
        self.frame_buttons.configure(relief='ridge',
                                     borderwidth=2,
                                     )
        self.frame_buttons.grid(row=0, column=0, padx=10, pady=10, sticky=('n', 'e', 's', 'w'))

        # FRAME FOR REPORTS
        self.frame_report = FrameReport(self.master)
        self.frame_report.configure(relief='ridge',
                                    borderwidth=2,
                                    )
        self.frame_report.grid(row=0, column=1, padx=5, pady=10, sticky=('n', 'e', 's', 'w'))

        # INFINITE LOOP
        self.master.mainloop()


class ButtonMenu(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        s = ttk.Style()
        s.configure('TButton',
                    width=20,
                    padding=10,
                    anchor='center',
                    font='arial 20',
                        )
        s.map('TButton',
                background=[('disabled', '#ccc'),
                            ('!active', '#009E2D'),
                            ('pressed', '#9BF0B7'), 
                            ('active', '#10EB4E'),
                            ],
                foreground=[('pressed', '#575757')]
                    )

        button_register = ttk.Button(self,
                                    text='CADASTRAR',
                                    command=lambda: TopLevelRegister(master),
                                    )
        button_register.grid(row=0, column=0, padx=10, pady=10)

        button_list = ttk.Button(self,
                                    text='RENDA FIXA',
                                    command=lambda: ListProducts(master))
        button_list.grid(row=1, column=0, padx=10, pady=10)

        button_sell = ttk.Button(self,
                                text='RENDA VARIÁVEL',
                                command=None,
                                )
        button_sell.grid(row=2, column=0, padx=10, pady=10)

        button_m_value = ttk.Button(self,
                                    text='ACERTAR VALOR',
                                    command=None,
                                    )
        button_m_value.grid(row=3, column=0, padx=10, pady=10)

        button_m_amount = ttk.Button(self,
                                    text='ACERTAR QTDE',
                                    command=None,
                                    )
        button_m_amount.grid(row=4, column=0, padx=10, pady=10)

        button_delete = ttk.Button(self,
                                    text='EXCLUIR',
                                    command=None,
                                    )
        button_delete.grid(row=5, column=0, padx=10, pady=10)


class FrameReport(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # LABELS FOR REPORTS
        s = ttk.Style()
        s.configure('L.TLabel', font='arial, 20', foreground='white')

        label_actions = ttk.Label(self,
                                  text=f'Total investido em Ações: R$ {self.report_actions()}',
                                  style='L.TLabel',
                                  )
        label_actions.grid(row=0, column=0, padx=5, pady=5)

        label_fii = ttk.Label(self,
                              text=f'Total investido em FIIs: R$ {self.report_fiis()}',
                              style='L.TLabel',
                              )
        label_fii.grid(row=1, column=0, padx=5, pady=5)

        label_direct_treasure = ttk.Label(self,
                                          text=f'Total investido no Tesouro Direto: R$ {self.report_direct_treasure()}',
                                          style='L.TLabel',
                                          )
        label_direct_treasure.grid(row=2, column=0, padx=5, pady=5)

        label_fixed_income = ttk.Label(self,
                                       text=f'Total investido em Renda Fixa: R$ {self.report_fixed_income()}',
                                       style='L.TLabel',
                                       )
        label_fixed_income.grid(row=3, column=0, padx=5, pady=5)

        label_emergency_reserve = ttk.Label(self,
                                            text=f'Total na Reserva de Emergência: R${self.report_emergency_reserv()}',
                                            style='L.TLabel',
                                            )
        label_emergency_reserve.grid(row=4, column=0, padx=5, pady=5)

        label_total_invest = ttk.Label(self,
                                       text=f'Total investido: R$ {self.report_total_invested()}',
                                       font='arial 24 bold',
                                       foreground='#009E2D',
                                       )
        label_total_invest.grid(row=5, column=0)
    
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
        self.top_level.configure(background='#000000')
        general_functions = GeneralFunctions()
        general_functions.set_size_window(self.top_level, 400, 400)

        button_fixed_income = ttk.Button(self.top_level,
                                         text='Renda Fixa',
                                         command=lambda: self.open_toplevel_fixed_income(master),
                                         )
        button_fixed_income.place(x=40, y=120)

        button_variable_income = ttk.Button(self.top_level,
                                            text='Renda Variável',
                                            command=lambda: self.open_toplevel_variable_income(master),
                                            )
        button_variable_income.place(x=40, y=190)
    
    # FUNCTIONS
    def open_toplevel_variable_income(self, master):
        self.top_level.destroy()
        sleep(1)
        TLRegVariableIncome(master,
                            'Cadastro Renda Variável',
                            '#000000',
                            580,
                            400,)
    
    def open_toplevel_fixed_income(self, master):
        self.top_level.destroy()
        sleep(1)
        TLRegFixedleIncome(master,
                           'Cadastro Renda Fixa',
                           '#000000',
                           535,
                           500,
                           )

class TLRegVariableIncome(Toplevel):
    def __init__(self, master, title, color, width, height):
        Toplevel.__init__(self, master)
        self.title(title)
        self.configure(background=color)
        GeneralFunctions().set_size_window(self, width, height)

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
        label_name = ttk.Label(self,
                               text='Nome:',
                               style='RV.TLabel'
                               )
        label_name.grid(row=0, column=0)

        self.entry_name = ttk.Entry(self,
                                    width=30,
                                    font='arial, 20',
                                    )
        self.entry_name.grid(row=0, column=1)

        # CODE
        label_code = ttk.Label(self,
                               text='Código',
                               style='RV.TLabel'
                               )
        label_code.grid(row=1, column=0)

        self.entry_code = ttk.Entry(self,
                                    width=30,
                                    font='arial 20',
                                    )
        self.entry_code.grid(row=1, column=1)

        # OPTIONS
        frame = ttk.Frame(self, style='RV.TFrame')
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
        frame_options = ttk.Frame(self, style='RV.TFrame')
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
            
            def check_data(data: tuple, step: int):
                for i in data:
                    if len(i) < step:
                        return False
                    else:
                        return True
            try:
                name = self.entry_name.get().title()
                code = self.entry_code.get().upper()

                if not check_data((name, code), 1):
                    showerror(message='Preencha todos os dados')
                    
                elif not check_data((code,), 5):
                    showerror(message='O código precisa ter pelo menos 5 caracteres')
                    
                else:
                    self.repository.criar_acao(name, code)
                    showinfo(message='Ativo cadastrado com sucesso.')
                    self.entry_name.delete(0, 'end')
                    self.entry_code.delete(0, 'end')
                    
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
                    self.entry_name.delete(0, 'end')
                    self.entry_code.delete(0, 'end')
                    
            except AtivoJaCadastradoError:
                showerror(message='Ativo já cadastrado no banco de dados')
                
        if not self.check_action and not self.check_fii:
            showerror(message='Preencha todos os dados')
        
    def quit(self):
        self.destroy()


class TLRegFixedleIncome(Toplevel):
    def __init__(self, master, title, color, width, height):
        Toplevel.__init__(self, master)
        self.title(title)
        self.configure(background=color)
        GeneralFunctions().set_size_window(self, width, height)

        # STYLES
        s = ttk.Style()
        s.configure('RF.TRadiobutton',
                    background='#000000',
                    foreground='white',
                    font='arial 20',
                    )
                    
        s.configure('RF.TFrame',
                    background='#000000',
                    )
        
        s.configure('RF.TLabel',
                    background='#000000',
                    foreground='white',
                    font='arila 20',
                    padding=10,
                    )
        
        s.configure('RFO.TButton', width=5, height=5, font='arial 5')

        # NAME
        label_name = ttk.Label(self,
                                text='Nome:',
                                style='RF.TLabel'
                                )
        label_name.grid(row=1, column=0)

        self.entry_name = ttk.Entry(self,
                                    width=20,
                                    font='arial 20',
                                    state='disabled',
                                    )
        self.entry_name.grid(row=1, column=1)

        # MONEY REDEMPTION
        label_redemption = ttk.Label(self,
                                          text='Resgate:',
                                          style='RF.TLabel',
                                          )
        label_redemption.grid(row=2, column=0)

        self.entry_redemption = ttk.Entry(self,
                                          width=15,
                                          font='arial 20',
                                          state='disabled',
                                          )
        self.entry_redemption.grid(row=2, column=1)

        # EXPIRATION
        label_expiration = ttk.Label(self,
                                    text='Vencimento:',
                                    style='RF.TLabel',
                                    )
        label_expiration.grid(row=3, column=0)

        self.entry_expiration = ttk.Entry(self,
                                          width=15,
                                          font='arial 20',
                                          state='disabled',
                                          )
        self.entry_expiration.grid(row=3, column=1)

        # PROFITABILITY
        label_profitability = ttk.Label(self,
                                       text='Rentabilidade:',
                                       style='RF.TLabel',
                                       )
        label_profitability.grid(row=4, column=0)

        self.entry_profitability = ttk.Entry(self,
                                          width=15,
                                          font='arial 20',
                                          state='disabled',
                                          )
        self.entry_profitability.grid(row=4, column=1)

        # PAYMENT
        self.frame_payment = ttk.Frame(self, style='RF.TFrame')
        self.frame_payment.grid(row=5, column=0, columnspan=2)
        
        label_payment = ttk.Label(self.frame_payment,
                                  text='Período dos pagamentos: ',
                                  style='RF.TLabel',
                                  )
        label_payment.pack(side='top')

        self.entry_payment = ttk.Entry(self.frame_payment,
                                      width=15,
                                      font='arial 20',
                                      state='!active',
                                      )

        # OPTIONS
        self.frame = ttk.Frame(self, style='RF.TFrame')
        self.frame.grid(row=0, column=0, columnspan=2, pady=(10, 0))
        
        self.options = ttk.Combobox(self.frame,
                                    values=('Renda Fixa',
                                            'Tesouro Direto',
                                            'Reserva de Emergência'),
                                    font='arial 18',
                                    )
        self.options.pack(side='left', padx=(0, 10))

        self.button_validate = ttk.Button(self.frame,
                                          text='V',
                                          command=self.select_option,
                                          style='RFO.TButton',
                                          )
        self.button_validate.pack(side='left')
        
        # BUTTONS TO CANCEL AND REGISTER
        self.frame_buttons = ttk.Frame(self, style='RF.TFrame')
        self.frame_buttons.grid(row=6, column=0, columnspan=2)
        
        self.button_cancel = ttk.Button(self.frame_buttons,
                                        text='CANCELAR',
                                        command=self.destroy,
                                        )
        self.button_cancel.grid(row=0, column=0, pady=(10))
        
        self.button_register = ttk.Button(self.frame_buttons,
                                          text='CADASTRAR',
                                          command=self.register,
                                          state='disabled',
                                          )
        self.button_register.grid(row=1, column=0)
    
    # FUNCTIONS    
    def select_option(self): 
        
        self.state = self.options.get()
        
        if self.state == 'Renda Fixa' or self.state == 'Reserva de Emergência':
            self.entry_name['state'] = 'normal'
            self.entry_redemption['state'] = 'normal'
            self.entry_expiration['state'] = 'normal'
            self.entry_profitability['state'] = 'normal'
            self.entry_payment['state'] = 'disabled'
            self.button_register['state'] = 'enabled'

        elif self.state == 'Tesouro Direto':
            self.entry_name['state'] = 'normal'
            self.entry_redemption['state'] = 'normal'
            self.entry_expiration['state'] = 'normal'
            self.entry_profitability['state'] = 'normal'
            self.entry_payment['state'] = 'normal'
            self.entry_payment.pack(side='top')
            self.button_register['state'] = 'enabled'

        else: 
            self.entry_name['state'] = 'disabled'
            self.entry_redemption['state'] = 'disabled'
            self.entry_expiration['state'] = 'disabled'
            self.entry_profitability['state'] = 'disabled'
            self.entry_payment['state'] = 'disabled'
            self.button_register['state'] = 'disabled'
    
    def register(self):
        self.rep_rf = AtivoFactory()
        
        name = self.entry_name.get().upper()
        redemption = self.entry_redemption.get().upper()
        expiration = self.entry_expiration.get().upper()
        profitability = self.entry_profitability.get().upper()
        payment = self.entry_payment.get().upper()
        
        list_one = [name, redemption, expiration, profitability]
        list_two = [name, redemption, expiration, profitability, payment]
        
        try:
            if self.state == 'Renda Fixa':
                if not self.check_one(list_one):
                    showerror(message='Verifique os dados informados')
                else:
                    self.rep_rf.criar_renda_fixa(name,
                                                redemption,
                                                expiration,
                                                profitability,
                                                )
                    self.entry_name.delete(0, 'end')
                    self.entry_redemption.delete(0, 'end')
                    self.entry_expiration.delete(0, 'end')
                    self.entry_profitability.delete(0, 'end')
                    showinfo(message='Ativo cadastrado com sucesso')
            
            elif self.state == 'Reserva de Emergência':
                if not self.check_one(list_one):
                    showerror(message='Verifique os dados informados')
                else:
                    self.rep_rf.criar_reserva_emergencia(name,
                                                        redemption,
                                                        expiration,
                                                        profitability,
                                                        )
                    self.entry_name.delete(0, 'end')
                    self.entry_redemption.delete(0, 'end')
                    self.entry_expiration.delete(0, 'end')
                    self.entry_profitability.delete(0, 'end')
                    showinfo(message='Ativo cadastrado com sucesso')
            
            elif self.state == 'Tesouro Direto':
                if not self.check_one(list_two):
                    showerror(message='Verifique os dados informados')
                else:
                    self.rep_rf.criar_tesouro_direto(name,
                                                    redemption,
                                                    expiration,
                                                    profitability,
                                                    payment,
                                                    )
                    self.entry_name.delete(0, 'end')
                    self.entry_redemption.delete(0, 'end')
                    self.entry_expiration.delete(0, 'end')
                    self.entry_profitability.delete(0, 'end')
                    self.entry_payment.delete(0, 'end')
                    showinfo(message='Ativo cadastrado com sucesso')
                
        except AtivoJaCadastradoError:
            showerror(message='Ativo já cadastrado na base de dados.')
    
    def check_one(self, list):
        amount: int = int(len(list))
        res_cont: int = int(sum([(1) for i in list if len(i) != 0]))
        if res_cont < amount:
            return False
        else:
            return True


class ListProducts(Toplevel):
    
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title('Ativos')
        self.configure(background='#000000')
        GeneralFunctions.set_size_window(self, 1200, 600)
        
        # VARIABLES
        self.rep_rf = RepositorioRendaFixa()

        # STYLES 
        s = ttk.Style()
        s.configure('Treeview', font='arial 14')
        s.configure('Heading', font='arial 14', foreground='white', background='black')
        s.configure('AT.TFrame', background='#000000')
        
        # COLUMNS OF TREEVIEW
        columns = ('id',
                   'nome',
                   'quantidade',
                   'categoria',
                   'resgate',
                   'valor_aplicado',
                   'vencimento',
                   'rentabilidade',
                   )
        
        # TREEVIEW
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=25)

        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='NOME')
        self.tree.heading('quantidade', text='QUANTIDADE')
        self.tree.heading('categoria', text='CATEGORIA')
        self.tree.heading('resgate', text='RESGATE')
        self.tree.heading('valor_aplicado', text='VALOR APLICADO')
        self.tree.heading('vencimento', text='VENCIMENTO')
        self.tree.heading('rentabilidade', text='RENTABILIDADE')

        self.tree.column(column=0, width=30, anchor='center', stretch=True)
        self.tree.column(column=1, anchor='center', stretch=True)
        self.tree.column(column=2, width=130, anchor='center', stretch=True)
        self.tree.column(column=3, width=140, anchor='center', stretch=True)
        self.tree.column(column=4, width=140, anchor='center', stretch=True)
        self.tree.column(column=5, anchor='center', stretch=True)
        self.tree.column(column=6, width=140, anchor='center', stretch=True)
        self.tree.column(column=7, anchor='center', stretch=True)

        # INSERT ITENS INTO TREEVIEW
        self.list_items()

        self.tree.grid(row=0, column=0, sticky=('n', 's', 'e', 'w'))
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # SCROLLBAR
        scroll = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky=('n', 's'))

        # FRAME FOR BUTTONS
        frame = ttk.Frame(self, style='AT.TFrame')
        frame.grid(row=1, column=0, columnspan=2)

        # BUTTONS
        self.button_purchase = ttk.Button(frame,
                                     text='Comprar',
                                     state='disabled',
                                     width=8,
                                     command=self.top_level_purchase,
                                     )
        self.button_purchase.grid(row=0, column=0, pady=(5, 10), padx=10)

        self.button_del = ttk.Button(frame,
                                      text='Deletar',
                                      state='disabled',
                                      width=8,
                                      command=self.top_level_del,
                                      )
        self.button_del.grid(row=0, column=1, pady=(5, 10), padx=10)

        self.button_redeem = ttk.Button(frame,
                                         text='Resgatar',
                                         state='disabled',
                                         width=8,
                                         command=self.top_level_redeem,
                                         )
        self.button_redeem.grid(row=0, column=2, pady=(5, 10), padx=10)

        self.button_change_data = ttk.Button(frame,
                                             text='Acertar valores',
                                             state='disabled',
                                             width=15,
                                             command=self.top_level_change_data,
                                             )
        self.button_change_data.grid(row=0, column=3, pady=(5, 10), padx=10)

    def list_items(self):
        for data in self.rep_rf.relatorio_for_tkinter():
            self.tree.insert('', 'end', values=data)
    
    def item_selected(self, *args):
        self.button_purchase['state'] = 'enable'
        self.button_del['state'] = 'enable'
        self.button_change_data['state'] = 'enable'
        self.button_redeem['state'] = 'enable'

        for selected_item in self.tree.selection():
            item: list = self.tree.item(selected_item)['values']
            return item
            
    def top_level_purchase(self):
        self.top_l = Toplevel(self)
        self.top_l.title('Comprar ativo')
        self.top_l.configure(background='#000000')
        GeneralFunctions.set_size_window(self.top_l, 400, 250)
        
        # STYLES
        s = ttk.Style()
        s.configure('TFrame', background='#000000')
        s.configure('TLabel',
                    background='#000000',
                    font='arial 16')
        
        # PRODUCT
        self.item: list = self.item_selected()        
        
        # FRAME
        frame = ttk.Frame(self.top_l)
        frame.grid(row=0, column=0, padx=(45, 0), pady=(20, 0))
        
        # FRAME_2
        frame_2 = ttk.Frame(self.top_l)
        frame_2.grid(row=1, column=0, padx=(45, 0), pady=(20, 0))
        
        # LABEL AND ENTRY FOR DATA
        label_id = ttk.Label(frame,
                             text='ID:',
                             )
        label_id.grid(row=0, column=0)
        
        entry_id = ttk.Entry(frame,
                             font='arial 16',
                             )
        entry_id.insert('end', self.item[0])
        entry_id.grid(row=0, column=1)
        
        label_name = ttk.Label(frame,
                               text='Nome:',
                               )
        label_name.grid(row=1, column=0)
        
        entry_name = ttk.Entry(frame,
                               font='arial 16',
                               )
        entry_name.insert('end', self.item[1])
        entry_name.grid(row=1, column=1)
        
        # LABEL AND ENTRY FOR PURCHASE        
        label_amount = ttk.Label(frame_2,
                                 text='Quantidade:',
                                 )
        label_amount.grid(row=0, column=0)
        
        self.amount_entry = ttk.Entry(frame_2,
                                 font='arial 16',
                                 width=6,
                                 )
        self.amount_entry.grid(row=0, column=1)
        
        label_value = ttk.Label(frame_2,
                                text='Valor:',
                                )
        label_value.grid(row=1, column=0)
        
        self.value_entry = ttk.Entry(frame_2,
                                font='arial 16',
                                width=6,
                                )
        self.value_entry.grid(row=1, column=1)
        
        # BUTTON FOR PURCHASE        
        button_purchase = ttk.Button(frame_2,
                                     text='Confirmar',
                                     width=10,
                                     command=self.purchase,
                                     )
        button_purchase.grid(row=2, column=0, columnspan=2, pady=(20, 0))
    
    def top_level_redeem(self):
        self.top_level_rdm = Toplevel(self)
        self.top_level_rdm.title('Acertar valores')
        self.top_level_rdm.configure(background='#000000')
        GeneralFunctions.set_size_window(self.top_level_rdm, 400, 250)
        
        # STYLES
        s = ttk.Style()
        s.configure('TFrame', background='#000000')
        s.configure('TLabel',
                    background='#000000',
                    font='arial 16')
        
        # PRODUCT
        self.item: list = self.item_selected()        
        
        # FRAME
        frame = ttk.Frame(self.top_level_rdm)
        frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        
        # FRAME_2
        frame_2 = ttk.Frame(self.top_level_rdm)
        frame_2.grid(row=1, column=0, padx=(20, 0), pady=(20, 0))
        
        # LABEL AND ENTRY FOR DATA
        label_name = ttk.Label(frame,
                               text='Nome:',
                               )
        label_name.grid(row=0, column=0)
        
        entry_name = ttk.Entry(frame,
                               font='arial 16',
                               )
        entry_name.grid(row=0, column=1)
        entry_name.insert('end', self.item[1])

        label_category = ttk.Label(frame,
                                   text='Categoria:',
                                   )
        label_category.grid(row=1, column=0)

        choices = ['Renda Fixa', 'Tesouro Direto', 'Reserva de Emergência']
        self.entry_category = ttk.Combobox(frame, values=choices, font='arial 14')
        self.entry_category.grid(row=1, column=1)
        self.entry_category.bind('<<ComboboxSelected>>', self.get_category)

        # BUTTON FOR CHANGE DATA  
        button_purchase = ttk.Button(frame_2,
                                     text='Confirmar',
                                     width=10,
                                     command=self.change_value_amount,
                                     )
        button_purchase.grid(row=2, column=0, columnspan=2, pady=(20, 0))
    
    def get_category(self):
        self.entry_category.select_clear()
        item = self.entry_category.get([0])
        print(item)
    
    def top_level_del(self):
        self.top_level_del = Toplevel(self)
        self.top_level_del.title('Deletar ativo')
        self.top_level_del.configure(background='#000000')
        GeneralFunctions.set_size_window(self.top_level_del, 400, 200)
        
        # STYLES
        s = ttk.Style()
        s.configure('TFrame', background='#000000')
        s.configure('TLabel',
                    background='#000000',
                    font='arial 16')
        
        # PRODUCT
        self.item: list = self.item_selected()        
        
        # FRAME
        frame = ttk.Frame(self.top_level_del)
        frame.grid(row=0, column=0, padx=(45, 0), pady=(20, 0))
        
        # FRAME_2
        frame_2 = ttk.Frame(self.top_level_del)
        frame_2.grid(row=1, column=0, padx=(45, 0), pady=(20, 0))
        
        # LABEL AND ENTRY FOR DATA
        label_id = ttk.Label(frame,
                             text='ID:',
                             )
        label_id.grid(row=0, column=0)
        
        entry_id = ttk.Entry(frame,
                             font='arial 16',
                             )
        entry_id.insert('end', self.item[0])
        entry_id.grid(row=0, column=1)
        
        label_name = ttk.Label(frame,
                               text='Nome:',
                               )
        label_name.grid(row=1, column=0)
        
        entry_name = ttk.Entry(frame,
                               font='arial 16',
                               )
        entry_name.insert('end', self.item[1])
        entry_name.grid(row=1, column=1)
        
        # BUTTON FOR SELL
        button_sell = ttk.Button(frame_2,
                                     text='Confirmar',
                                     width=10,
                                     command=self.sell,
                                     )
        button_sell.grid(row=2, column=0, columnspan=2, pady=(20, 0))
    
    def top_level_change_data(self):
        self.top_level_change = Toplevel(self)
        self.top_level_change.title('Acertar valores')
        self.top_level_change.configure(background='#000000')
        GeneralFunctions.set_size_window(self.top_level_change, 400, 250)
        
        # STYLES
        s = ttk.Style()
        s.configure('TFrame', background='#000000')
        s.configure('TLabel',
                    background='#000000',
                    font='arial 16')
        
        # PRODUCT
        self.item: list = self.item_selected()        
        
        # FRAME
        frame = ttk.Frame(self.top_level_change)
        frame.grid(row=0, column=0, padx=(45, 0), pady=(20, 0))
        
        # FRAME_2
        frame_2 = ttk.Frame(self.top_level_change)
        frame_2.grid(row=1, column=0, padx=(45, 0), pady=(20, 0))
        
        # LABEL AND ENTRY FOR DATA
        label_id = ttk.Label(frame,
                             text='ID:',
                             )
        label_id.grid(row=0, column=0)
        
        entry_id = ttk.Entry(frame,
                             font='arial 16',
                             )
        entry_id.insert('end', self.item[0])
        entry_id.grid(row=0, column=1)
        
        label_name = ttk.Label(frame,
                               text='Nome:',
                               )
        label_name.grid(row=1, column=0)
        
        entry_name = ttk.Entry(frame,
                               font='arial 16',
                               )
        entry_name.insert('end', self.item[1])
        entry_name.grid(row=1, column=1)

        label_amount = ttk.Label(frame_2,
                                 text='Quantidade:',
                                 )
        label_amount.grid(row=0, column=0)
        
        self.amount_entry = ttk.Entry(frame_2,
                                 font='arial 16',
                                 width=12,
                                 )
        self.amount_entry.grid(row=0, column=1)
        self.amount_entry.insert('end', self.item[2])
        
        label_value = ttk.Label(frame_2,
                                text='Valor:',
                                )
        label_value.grid(row=1, column=0)
        
        self.value_entry = ttk.Entry(frame_2,
                                font='arial 16',
                                width=12,
                                )
        self.value_entry.grid(row=1, column=1)
        self.value_entry.insert('end', self.item[5])
        
        # BUTTON FOR CHANGE DATA  
        button_purchase = ttk.Button(frame_2,
                                     text='Confirmar',
                                     width=10,
                                     command=self.change_value_amount,
                                     )
        button_purchase.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
    def purchase(self):
        amount = self.amount_entry.get()
        value = self.value_entry.get().replace(',', '.')
        code: str = str(self.item[1])
                
        try:
            if not amount or not value or amount =='' or value == '':
                showerror(message="Verifique a quantidade e valor informados")
                return
            else:
                self.rep_rf.comprar(code, int(amount), float(value))
                showinfo(message=f'Compra realizada com sucesso')
                self.top_l.destroy()
        except ValueError:
            showerror(message='Entrada de dados inválida')
        except Exception as error:
            showerror(message=f'Error: {error}')
    
    def sell(self):
        code: str = str(self.item[1])
        try:
            self.rep_rf.deletar_ativo(code)
            showinfo(message=f'Ativo deletado com sucesso')
            self.top_level_del.destroy()
        except Exception as error:
            showerror(message=f'Error: {error}')
    
    def change_value_amount(self):
        code: str = str(self.item[1])
        amount = self.amount_entry.get()
        value = self.value_entry.get().replace(',', '.')

        try:
            if not amount or not value or amount =='' or value == '':
                showerror(message="Verifique a quantidade e valor informados")
                return
            else:
                self.rep_rf.acertar_valor_aplicado(code, float(value), int(amount))
                showinfo(message=f'Dados alterados com sucesso')
                self.top_level_change.destroy()
        except ValueError:
            showerror(message='Entrada de dados inválida')
        except Exception as error:
            showerror(message=f'Error: {error}')
        




class GeneralFunctions:
    @staticmethod
    def set_size_window(window, width, height):
        w = int((window.winfo_screenwidth() / 2) - (width/2))
        h = int((window.winfo_screenheight() / 2) - (height/2))
        window.geometry(f'{width}x{height}+{w}+{h}')


PyInvest()
