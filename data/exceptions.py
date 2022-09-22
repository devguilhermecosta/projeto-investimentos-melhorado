class AtivoJaCadastradoError(BaseException):
    def __init__(self, msg: str) -> None:
        self.msg: str = msg

    def __str__(self) -> str:
        return self.msg


class AtivoNaoCadastradoError(BaseException):
    def __init__(self, msg: str) -> None:
        self.msg: str = msg
        
    def __str__(self) -> str:
        return self.msg


class QuantidadeInsuficienteError(BaseException):
    def __init__(self, msg: str) -> str:
        self.msg: str = msg
        
    def __str__(self) -> str:
        return self.msg


class SaldoInsuficienteError(BaseException):
    def __init__(self, msg: str):
        self.msg: str = msg
        
    def __str__(self) -> str:
        return self.msg
