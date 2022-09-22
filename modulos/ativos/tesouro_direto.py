from .ativo import AtivoRendaFixa


class TesouroDireto(AtivoRendaFixa):
    def __init__(self, 
                 nome: str, 
                 resgate: str, 
                 vencimento: str,
                 rentabilidade: str, 
                 periodicidade_pagamentos: str,
                 categoria: str = 'Tesouro Direto',):
        super().__init__(nome, resgate, vencimento, rentabilidade, categoria)
        self.__periodicidade_pagamentos: str = periodicidade_pagamentos
    
    @property
    def periodicidade_pagamentos(self) -> str:
        return self.__periodicidade_pagamentos

    def __str__(self):
        resultado = super().__str__()
        resultado += f'Periodicidade dos pagamentos: {self.periodicidade_pagamentos}\n'
        return resultado
