try:
    import sys
    import os
    
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
from ativos.fiis import Fiis
from ativos.acoes import Acao
from ativos.renda_fixa import RendaFixa
from ativos.tesouro_direto import TesouroDireto
from ativos.reserva_emergencia import ReservaEmergencia


class MetodosSqlRV:
    def __init__(self):
        self._conn = sq.connect('data/data.db')
        self._cursor = self._conn.cursor()
        
    def _existe_ativo(self, codigo: str) -> bool:
        """
        Param: codigo: str
        return: bool
        """
        resultado: bool = False
        self.__sub_acao_sql_select_all_com_codigo(codigo)
        for i in self._cursor.fetchall():
            if i[2] == codigo:
                resultado = True
        return resultado

    def _get_id_rv(self, codigo: str) -> int:
        """
        Param: codigo: str
        return: int
        """
        resultado: int = -1
        if self._existe_ativo(codigo):
            self.__sub_acao_sql_select_all_com_codigo(codigo)
            for i in self._cursor.fetchall():
                if i[2] == codigo:
                    resultado = i[0]
        return resultado

    def _quantidade_suficiente(self, ativo: Acao | Fiis) -> bool:
        """
        Param: ativo: Object -> Acao | Fiis
        Param: nome: str
        Param: codigo: str
    
        return bool
        """
        resultado: bool = False
        if self._existe_ativo(ativo.codigo):
            self.__sub_acao_sql_select_all_com_id(ativo)
            for at in self._cursor.fetchall():
                quantidade_disponivel: int = at[4]
                
            if quantidade_disponivel > 0:
                resultado = True
        return resultado

    def acao_sql_cadastrar_ativo(self, ativo: Acao | Fiis) -> None:
        acao = "INSERT INTO RV" \
                    "(nome, codigo, categoria, quantidade, PU, PM, PT)" \
                    "VALUES (?, ?, ?, ?, ?, ?, ?)"
        self._cursor.execute(acao, 
                                 (ativo.nome,
                                 ativo.codigo,
                                 ativo.categoria,
                                 ativo.quantidade,
                                 ativo.preco_unitario,
                                 ativo.preco_medio,
                                 ativo.preco_total)
                                 )
        self._conn.commit()

    def acao_aql_comprar_ativo(self, ativo: Fiis | Acao, qtde: int, pu: float) -> None:
        self.__sub_acao_sql_select_all_com_id(ativo)

        for at in self._cursor.fetchall():
            qtde_atual: int = at[4]
            pm_atual: float = at[6]
            
            nova_qtde: int = qtde_atual + qtde
            novo_pu: float = pu
            if pm_atual <= 0:
                novo_pm: float = pu
            else:
                novo_pm = (pm_atual + pu) / 2
            novo_pt: float = novo_pm * nova_qtde
            
            acao_2 = "UPDATE RV SET quantidade=?, PU=?, PM=?, PT=? WHERE id=?"
            self._cursor.execute(acao_2, (nova_qtde, novo_pu, novo_pm, novo_pt, at[0]))
            self._conn.commit()

    def acao_sql_vender(self, ativo: Acao | Fiis, qtde: int, pu: float) -> None:
        self.__sub_acao_sql_select_all_com_id(ativo)
        
        for at in self._cursor.fetchall():
            qtde_atual: int = at[4]
            pm_atual: float = at[6]
            
            nova_qtde: int = qtde_atual - qtde
            novo_pu: float = pu
            if pm_atual <= 0:
                novo_pm: float = pu
            else:
                novo_pm = (pm_atual + pu) / 2 
            novo_pt: float = novo_pm * nova_qtde
            
            acao_2 = "UPDATE RV SET quantidade=?, PU=?, PM=?, PT=? WHERE id=?"
            self._cursor.execute(acao_2, (nova_qtde, novo_pu, novo_pm, novo_pt, at[0]))
            self._conn.commit()

    def acao_sql_deletar_ativo(self, ativo: Acao | Fiis) -> None:
        ident = self._get_id_rv(ativo.codigo)
        acao = "DELETE FROM RV WHERE id=?"
        self._cursor.execute(acao, (ident,))
        self._conn.commit()

    def acao_sql_alterar_dados(self, ativo: Acao | Fiis, nome: str, codigo: str) -> None:
        ident: int = self._get_id_rv(ativo.codigo)
        acao = "UPDATE RV SET nome=?, codigo=? WHERE id=?"
        self._cursor.execute(acao, (nome, codigo, ident))
        self._conn.commit()

    def acao_sql_acertar_quantidade(self, ativo: Acao | Fiis, qtde: int) -> None:
        ident: int = self._get_id_rv(ativo.codigo)
        acao = "UPDATE RV SET quantidade=? WHERE id=?"
        self._cursor.execute(acao, (qtde, ident))
        self._conn.commit()

    def acao_sql_acertar_preco_unit(self, ativo: Acao | Fiis, pu: float) -> None:
        ident: int = self._get_id_rv(ativo.codigo)
        acao = "UPDATE RV SET PU=? WHERE id=?"
        self._cursor.execute(acao, (pu, ident))
        self._conn.commit()

    def __sub_acao_sql_select_all_com_id(self, ativo: Acao | Fiis) -> None:
        ident: int = self._get_id_rv(ativo.codigo)
        acao = "SELECT * FROM RV WHERE id=?"
        self._cursor.execute(acao, (ident,))
        
    def __sub_acao_sql_select_all_com_codigo(self, codigo: str) -> None:
        acao: str = 'SELECT * FROM RV WHERE codigo=?'
        self._cursor.execute(acao, (codigo,))

    def sair(self) -> None:
        self._conn.close()


class MetodosSqlRF:
    def __init__(self):
        self._conn = sq.connect('data/data.db')
        self._cursor = self._conn.cursor()
        
    def _existe(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> bool:
        """
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia
        return bool
        """        
        if self._get_id(ativo) != -1:
            return True
        else:
            return False
    
    def _get_id(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> int:
        """      
        Param: ativo: Object -> RendaFixa | TesouroDireto | ReservaEmergencia
        return int -> -1 se não existir ou o próprio id
        """
        resultado: int = -1
        acao: str = "SELECT * FROM RF WHERE nome=?"
        self._cursor.execute(acao, (ativo.nome,))
        for at in self._cursor.fetchall():
            if at[1] == ativo.nome:
                resultado = at[0]       
        return resultado

    def acao_sql_alterar_saldo_apos_resgate(self,
                                              ativo: RendaFixa | TesouroDireto | ReservaEmergencia,
                                              qtde: int,
                                              valor: float) -> None:
        self.__sub_acao_sql_select_all_com_id(ativo)
        for at in self._cursor.fetchall():
            qtde_atual: int = at[2]
            saldo_atual: float = at[5]
            
            if (qtde_atual - qtde) <= 0:
                nova_qtde: int = 1
            else:
                nova_qtde = qtde_atual - qtde
            novo_saldo: float = saldo_atual - valor
        
        acao_2: str = "UPDATE RF SET quantidade=?, valor_aplicado=? WHERE id=?"
        self._cursor.execute(acao_2, (nova_qtde, novo_saldo, at[0]))
        self._conn.commit()
            
    def acao_sql_get_saldo(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> float | int:
        self.__sub_acao_sql_select_all_com_id(ativo)
        for at in self._cursor.fetchall():
            saldo: int | float = at[5]
        return saldo

    def acao_sql_insert(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> None:
        acao = "INSERT INTO RF" \
                "(nome, quantidade, categoria, resgate, valor_aplicado, vencimento, rentabilidade)" \
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
        self._cursor.execute(acao, (ativo.nome,
                                    ativo.quantidade,
                                    ativo.categoria,
                                    ativo.resgate,
                                    ativo.valor_aplicado,
                                    ativo.vencimento,
                                    ativo.rentabilidade)
                                )
        self._conn.commit()
                
    def acao_sql_comprar(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia, qtde: int, valor: float) -> None:
        self.__sub_acao_sql_select_all_com_id(ativo)
        for at in self._cursor.fetchall():
            qtde_atual: int = at[2]
            valor_atual: float = at[5]
            
            nova_qtde: int = qtde_atual + qtde
            novo_valor: float = valor_atual + valor
            
            acao_2: str = "UPDATE RF SET quantidade=?, valor_aplicado=? WHERE id=?"
            self._cursor.execute(acao_2, (nova_qtde, novo_valor, at[0]))
            self._conn.commit()
            
    def acao_sql_alterar_dados(self,
                                 ativo: RendaFixa | TesouroDireto | ReservaEmergencia,
                                 nome: str,
                                 data_resgate: str,
                                 data_vencimento: str,
                                 rentabilidade: str) -> None:
            self.__sub_acao_sql_select_all_com_id(ativo)
            for at in self._cursor.fetchall():
                n_nome: str = nome
                n_data_resgate: str = data_resgate
                n_vencimento: str = data_vencimento
                n_rent: str = rentabilidade
                
                acao_2: str = "UPDATE RF SET nome=?, resgate=?, vencimento=?, rentabilidade=? WHERE id=?"
                self._cursor.execute(acao_2, (n_nome, n_data_resgate, n_vencimento, n_rent, at[0]))
                self._conn.commit()
    
    def acao_sql_acertar_valor_aplicado(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia, valor: float) -> None:
        self.__sub_acao_sql_select_all_com_id(ativo)      
        for at in self._cursor.fetchall():
            novo_valor: float = valor

            acao_2: str = "UPDATE RF SET valor_aplicado=? WHERE id=?"
            self._cursor.execute(acao_2, (novo_valor, at[0]))
            self._conn.commit()
            
    def acao_sql_deletar_ativo(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> None:
        ident: int = self._get_id(ativo)
            
        acao = "DELETE FROM RF WHERE id=?"
        self._cursor.execute(acao, (ident,))
        self._conn.commit()
        
    def __sub_acao_sql_select_all_com_id(self, ativo: RendaFixa | TesouroDireto | ReservaEmergencia) -> None:
        ident: int = self._get_id(ativo)
        acao: str = "SELECT * FROM RF WHERE id=?"
        self._cursor.execute(acao, (ident,))
        
    def sair(self) -> None:
        self._conn.close()
