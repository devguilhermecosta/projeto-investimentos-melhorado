from data.data import RepositorioRendaFixa, RepositorioRendaVariavel
from modulos.ativos.acoes import Acao
from modulos.ativos.fiis import Fiis
from modulos.ativos.renda_fixa import RendaFixa
from modulos.ativos.tesouro_direto import TesouroDireto
from modulos.ativos.reserva_emergencia import ReservaEmergencia

"""
A ideia aqui é criar uma fábrica que retorna objetos prontos,
fazendo com o que o usuário não instancie a classe diretamente,
tento um baixo acoplamento intre a interface e o usuário.
"""


class AtivoFactory:
    def __init__(self):
        self.rep_rv = RepositorioRendaVariavel()
        self.rep_rf = RepositorioRendaFixa()

    def criar_acao(self, nome: str, codigo: str) -> Acao:
        self.rep_rv.cadastrar_ativo(Acao(nome, codigo))

    def criar_fii(self, nome: str, codigo: str) -> Fiis:
        self.rep_rv.cadastrar_ativo(Fiis(nome, codigo))
    
    def criar_renda_fixa(self,
                         nome: str,
                         resgate: str,
                         vencimento: str,
                         rentabilidade: str) -> RendaFixa:
        self.rep_rf.cadastrar_ativo(RendaFixa(nome, resgate, vencimento, rentabilidade))
    
    def criar_tesouro_direto(self,
                             nome: str,
                             resgate: str,
                             vencimento: str,
                             rentabilidade: str,
                             periodicidade_pagamentos: str) -> TesouroDireto:
        self.rep_rf.cadastrar_ativo(TesouroDireto(nome,
                                                  resgate,
                                                  vencimento,
                                                  rentabilidade,
                                                  periodicidade_pagamentos))

    def criar_reserva_emergencia(self,
                                 nome: str,
                                 resgate: str,
                                 vencimento: str,
                                 rentabilidade: str) -> ReservaEmergencia:
        self.rep_rf.cadastrar_ativo(ReservaEmergencia(nome,
                                                      resgate,
                                                      vencimento,
                                                      rentabilidade))
