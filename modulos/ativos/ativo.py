from abc import ABC


class AtivoAcoesFiis(ABC):
    def __init__(self, nome: str, codigo: str, categoria: str) -> None:
        self.__nome: str = nome
        self.__codigo: str = codigo
        self.__categoria: str = categoria
        self.__quantidade: int = 0
        self.__preco_unitario: float = 0.0
        self.__preco_medio: float = 0.0
        self.__preco_total: float = 0.0

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def categoria(self) -> str:
        return self.__categoria

    @property
    def preco_unitario(self) -> float:
        return self.__preco_unitario

    @property
    def preco_medio(self) -> float:
        return self.__preco_medio
    
    @property
    def preco_total(self) -> float:
        return self.__preco_total

    @property
    def quantidade(self) -> int:
        return self.__quantidade

    def __repr__(self):
        resultado = f'Nome: {self.nome}\n'
        resultado += f'Codigo: {self.codigo}\n'
        resultado += f'Quantidade: {self.quantidade}\n'
        resultado += f'Categoria: {self.categoria}\n'
        resultado += f'Preço Unitário: {self.preco_unitario}\n'
        resultado += f'Preço Médio: {self.preco_medio}\n'
        return resultado


class AtivoRendaFixa(ABC):
    def __init__(self, nome: str,
                 resgate: str,
                 vencimento: str,
                 rentabilidade: str,
                 categoria: str,):
        self.__nome: str = nome
        self.__quantidade: float = 0.0
        self.__categoria: str = categoria
        self.__resgate: str = resgate
        self.__valor_aplicado: float = 0.0
        self.__vencimento: str = vencimento
        self.__rentabilidade: str = rentabilidade

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @property
    def categoria(self) -> str:
        return self.__categoria

    @property
    def resgate(self) -> str:
        return self.__resgate

    @property
    def valor_aplicado(self) -> float:
        return self.__valor_aplicado

    @property
    def vencimento(self) -> str:
        return self.__vencimento

    @property
    def rentabilidade(self) -> str:
        return self.__rentabilidade

    def __str__(self):
        resultado = f'Nome: {self.nome}\n'
        resultado += f'Quantidade: {self.quantidade}\n'
        resultado += f'Categoria: {self.categoria}\n'
        resultado += f'Valor aplicado: {self.valor_aplicado}\n'
        resultado += f'Resgate: {self.resgate}\n'
        resultado += f'Vencimento: {self.vencimento}\n'
        resultado += f'Rentabilidade: {self.rentabilidade}\n'
        return resultado
