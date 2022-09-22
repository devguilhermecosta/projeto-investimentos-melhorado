from .ativo import AtivoRendaFixa


class ReservaEmergencia(AtivoRendaFixa):
    def __init__(self,
                 nome: str,
                 resgate: str,
                 vencimento: str,
                 rentabilidade: str,
                 categoria: str = 'Reserva de Emergência'):
        super().__init__(nome, resgate, vencimento, rentabilidade, categoria)
