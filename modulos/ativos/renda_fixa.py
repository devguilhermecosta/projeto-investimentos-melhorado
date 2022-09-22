from .ativo import AtivoRendaFixa


class RendaFixa(AtivoRendaFixa):
    def __init__(self,
                 nome: str,
                 resgate: str,
                 vencimento: str,
                 rentabilidade: str,
                 categoria: str = 'Renda Fixa'):
        super().__init__(nome, resgate, vencimento, rentabilidade, categoria)
