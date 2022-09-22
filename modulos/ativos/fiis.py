from .ativo import AtivoAcoesFiis


class Fiis(AtivoAcoesFiis):
    def __init__(self, nome: str, codigo: str, categoria: str = 'FIIs'):
        super().__init__(nome, codigo, categoria)
