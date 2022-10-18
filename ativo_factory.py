from data.data import RepositorioRendaFixa, RepositorioRendaVariavel
from modulos.ativos.acoes import Acao
from modulos.ativos.fiis import Fiis
from modulos.ativos.renda_fixa import RendaFixa
from modulos.ativos.reserva_emergencia import ReservaEmergencia
from modulos.ativos.tesouro_direto import TesouroDireto


class AtivoFactory:
    def __init__(self):
        self.__rep_rv = RepositorioRendaVariavel()
        self.__rep_rf = RepositorioRendaFixa()
    
    def conectar_bd_rf(self) -> RepositorioRendaFixa:
        return self.__rep_rf
    
    def conectar_bd_rv(self) -> RepositorioRendaVariavel:
        return self.__rep_rv

    def criar_acao(self, nome: str, codigo: str) -> Acao:
        self.__rep_rv.cadastrar_ativo(Acao(nome, codigo))

    def criar_fii(self, nome: str, codigo: str) -> Fiis:
        self.__rep_rv.cadastrar_ativo(Fiis(nome, codigo))
    
    def criar_renda_fixa(self,
                         nome: str,
                         resgate: str,
                         vencimento: str,
                         rentabilidade: str) -> RendaFixa:
        self.__rep_rf.cadastrar_ativo(RendaFixa(nome, resgate, vencimento, rentabilidade))
    
    def criar_tesouro_direto(self,
                             nome: str,
                             resgate: str,
                             vencimento: str,
                             rentabilidade: str,
                             periodicidade_pagamentos: str) -> TesouroDireto:
        self.__rep_rf.cadastrar_ativo(TesouroDireto(nome,
                                                  resgate,
                                                  vencimento,
                                                  rentabilidade,
                                                  periodicidade_pagamentos))

    def criar_reserva_emergencia(self,
                                 nome: str,
                                 resgate: str,
                                 vencimento: str,
                                 rentabilidade: str) -> ReservaEmergencia:
        self.__rep_rf.cadastrar_ativo(ReservaEmergencia(nome,
                                                      resgate,
                                                      vencimento,
                                                      rentabilidade))
