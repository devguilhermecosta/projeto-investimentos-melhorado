from .ativo import AtivoAcoesFiis


class Acao(AtivoAcoesFiis):
    def __init__(self, nome: str, codigo: str, categoria: str = 'Ações'):
        super().__init__(nome, codigo, categoria)
