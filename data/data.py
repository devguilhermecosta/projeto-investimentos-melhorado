try:
    import os
    import sys
    
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../modulos'
            )
        )
    )
except Exception as error:
    print(f'{error}')


import sqlite3 as sq

from ativos.acoes import Acao
from ativos.fiis import Fiis
from ativos.renda_fixa import RendaFixa
from ativos.reserva_emergencia import ReservaEmergencia
from ativos.tesouro_direto import TesouroDireto

from .exceptions import (AtivoJaCadastradoError, AtivoNaoCadastradoError,
                         QuantidadeInsuficienteError, SaldoInsuficienteError)
from .metodos_sql import MetodosSqlRF, MetodosSqlRV


class RepositorioRendaVariavel(MetodosSqlRV):
    def cadastrar_ativo(self, ativo: Acao | Fiis) -> int | None:
        """       
        Param: ativo: Object -> Acao | Fiis
        
        Raise: AtivoJaCadastradoError
              
        return 0 or None
        """
        if self._existe_ativo(ativo.codigo):
            raise AtivoJaCadastradoError('Ativo já cadastrado.')
        else:
            self.acao_sql_cadastrar_ativo(ativo)
            return 0
    
    def comprar(self, id: str, qtde: int, pu: float) -> int | None:
        """
        Param: ativo: Object -> Acao | Fiis
        Param: qtde: int
        Param: pu: float
        
        Raise: AtivoNaoCadastradoError
        
        return 0 or None
        """      
        try:
            self.acao_aql_comprar_ativo(id, qtde, pu)
        except Exception as error:
            print(error)
            
    def vender(self, id: str, qtde: int, pu: float) -> None:
        """
        Param: id: str
        Param: qtde: int
        Param: pu: float
        
        Raise: QuantidadeInsuficienteError
        
        return None
        """
        try:
            self.acao_sql_vender(id, qtde, pu)
        except QuantidadeInsuficienteError:
            raise QuantidadeInsuficienteError('Quantidade insuficiente para venda')
      
    def deletar(self, id: str) -> int:
        """
        Param: id: str
        
        return 0 or None
        """
        try:
            self.acao_sql_deletar_ativo(id)
            return 0
        except Exception as error:
            print(error)

    def alterar_dados(self, id: str, nome: str, codigo: str, categoria: str) -> int | None:
        """       
        Param: id: str
        Param: nome: str
        Param: codigo: str
        Param: categoria: str
           
        return 0 or None
        """
        self.acao_sql_alterar_dados(id, nome, codigo, categoria)
        return 0


    def acertar_valor_quantidade(self, id: str, qtde: int, pu: float) -> int | None:
        """
        Param: id: str
        Param: qtde: int
        Param: pu: float
        
        return 0 or None
        """
        self.acao_sql_acertar_valor_qtde(id, qtde, pu)
        return 0
    
    def relatorio_acoes(self):
        acao: str = "SELECT * FROM RV"
        self._cursor.execute(acao)
        tot: int | float = 0

        for item in self._cursor.fetchall():
            if item[3] == 'Ações':
                tot += float(item[7])

        return tot
    
    def relatorio_fiis(self):
        acao: str = "SELECT * FROM RV"
        self._cursor.execute(acao)
        tot: int | float = 0

        for item in self._cursor.fetchall():
            if item[3] == 'FIIs':
                tot += float(item[7])

        return tot

    def relatorio_for_tkinter(self) -> list:
        acao: str = "SELECT * FROM RV"
        self._cursor.execute(acao)
        rep: list = []

        for i in self._cursor.fetchall():
            res: list = [i[0], i[1], i[2], i[3], i[4], f'R$ {i[5]:.2f}', f'R$ {i[6]:.2f}', f'R$ {i[7]:.2f}']
            rep.append(res)
        return rep


class RepositorioRendaFixa(MetodosSqlRF):      
    def cadastrar_ativo(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> int | None:
        """
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia  
        
        Raise: AtivoJaCadastradoError   
        
        return 0 or None
        """        
        if self._existe(ativo):
            raise AtivoJaCadastradoError('Ativo já cadastrado')
        else:
            self.acao_sql_insert(ativo)
        return 0
    
    def comprar(self,
                ativo: RendaFixa | TesouroDireto | ReservaEmergencia,
                qtde: int,
                valor: float) -> int:
        """
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia
        Param: qtde: int
        Param: valor: float
        
        Raise: AtivoNaoCadastradoError
        
        return int -> -1 se não comprado ou 0 se comprado
        """
        resultado: int = -1
        try:
            self.acao_sql_comprar(ativo, qtde, valor)
        except AtivoNaoCadastradoError:
            print('Ativo não cadastrado')
    
    def resgatar(self,
                 ativo: RendaFixa | TesouroDireto | ReservaEmergencia,
                 qtde: int,
                 valor: float) -> int | None:
        """
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia
        Param: qtde: int
        Param: valor: float
        
        Raise: AtivoNaoCadastradoError, SaldoInsuficienteError
        
        return 0 or None
        """
        if not self._existe(ativo):
            raise AtivoNaoCadastradoError('Ativo não cadastrado')
        elif self.acao_sql_get_saldo(ativo) <= 0:
            raise SaldoInsuficienteError('Saldo insuficiente para resgate')
        else:
            self.acao_sql_alterar_saldo_apos_resgate(ativo, qtde, valor)
            return 0
        
    def alterar_dados_ativo(self,
                             id: str,
                             nome: str,
                             categoria: str,
                             data_resgate: str,
                             data_vencimento: str,
                             rentabilidade: str) -> int | None:
        """
        Param: ativo: id or code
        Param: nome: str
        Param: data_resgate: str
        Param: data_vencimento: str
        Param: rentabilidade: str
        
        Raise: AtivoNaoCadastradoError
        
        return 0 or None
        """
        try:
            self.acao_sql_alterar_dados(id, nome, categoria, data_resgate, data_vencimento,
                                        rentabilidade)
        except AtivoNaoCadastradoError:
            print('Ativo não cadastrado')
        
    def acertar_valor_aplicado(self,
                               ativo: RendaFixa | TesouroDireto | ReservaEmergencia,
                               valor: float,
                               quantidade) -> int | None:
        """
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia
        Param: valor: float
        
        Raise: AtivoNaoCadastradoError
        
        return 0 or None
        """
        try:
            self.acao_sql_acertar_valor_aplicado(ativo, valor, quantidade)
        except AtivoNaoCadastradoError:
            print('Ativo não cadastrado')
        
    def deletar_ativo(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> int | None:
        """
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia
            
        Raise: AtivoNaoCadastradoError
        
        return 0 or None
        """
        if not self._existe(ativo):
            raise AtivoNaoCadastradoError('Ativo não cadastrado')
        else:
            self.acao_sql_deletar_ativo(ativo)
            return 0
    
    def relatorio_res_emerg(self) -> int | float:
        acao: str = "SELECT * FROM RF"
        self._cursor.execute(acao)
        tot: int | float = 0

        for item in self._cursor.fetchall():
            if item[3] == 'Reserva de Emergência':
                tot += float(item[5])

        return tot
    
    def relatorio_tesouro_direto(self) -> int | float:
        acao: str = "SELECT * FROM RF"
        self._cursor.execute(acao)
        tot: int | float = 0

        for item in self._cursor.fetchall():
            if item[3] == 'Tesouro Direto':
                tot += float(item[5])
        
        return tot

    def relatorio_renda_fixa(self) -> int | float:
        acao: str = "SELECT * FROM RF"
        self._cursor.execute(acao)
        tot: int | float = 0

        for item in self._cursor.fetchall():
            if item[3] == 'Renda Fixa':
                tot += float(item[5])
        
        return tot

    def relatorio_for_tkinter(self) -> list:
        acao: str = "SELECT * FROM RF"
        self._cursor.execute(acao)
        rep: list = []

        for i in self._cursor.fetchall():
            res: list = [i[0], i[1], i[2], i[3], i[4], f'R$ {i[5]:.2f}', i[6], i[7]]
            rep.append(res)
        return rep
