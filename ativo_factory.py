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
    
    @staticmethod
    def criar_acao(nome: str, codigo: str) -> Acao:
        return Acao(nome, codigo)
    
    @staticmethod
    def criar_fii(nome: str, codigo: str) -> Fiis:
        return Fiis(nome, codigo)
    
    @staticmethod
    def criar_renda_fixa(nome: str,
                         resgate: str,
                         vencimento: str,
                         rentabilidade: str) -> RendaFixa:
        return RendaFixa(nome, resgate, vencimento, rentabilidade)
    
    @staticmethod
    def criar_tesouro_direto(nome: str,
                             resgate: str,
                             vencimento: str,
                             rentabilidade: str,
                             periodicidade_pagamentos: str) -> TesouroDireto:
        return TesouroDireto(nome,
                             resgate,
                             vencimento,
                             rentabilidade,
                             periodicidade_pagamentos)
        
    @staticmethod
    def criar_reserva_emergencia(nome: str,
                                 resgate: str,
                                 vencimento: str,
                                 rentabilidade: str) -> ReservaEmergencia:
        return ReservaEmergencia(nome, resgate, vencimento, rentabilidade)
