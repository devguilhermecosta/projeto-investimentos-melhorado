try:
    import sys
    import os

    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../modulos'
            )
        )
    )
except Exception as error:
    print(f'{error}')

import unittest
from ativos.acoes import Acao


class TesteCategoriaAcoes(unittest.TestCase):
    def setUp(self):
        self.acao = Acao('Banco do Brasil', 'BBAS3')
        
    def test_classe_acao_attr_nome_deve_ser_string(self):
        self.assertIsInstance(self.acao.nome, str)
        
    def test_classe_acao_attr_codigo_deve_ser_string(self):
        self.assertIsInstance(self.acao.codigo, str)
        
    def test_classe_acao_attr_categoria_deve_ser_string(self):
        self.assertIsInstance(self.acao.categoria, str)
        
    def test_classe_acao_attr_quantidade_deve_ser_int(self):
        self.assertIsInstance(self.acao.quantidade, int)  
              
    def test_classe_acao_attr_preco_unitario_deve_ser_float(self):
        self.assertIsInstance(self.acao.preco_unitario, float)

    def test_classe_acao_attr_preco_medio_deve_ser_float(self):
        self.assertIsInstance(self.acao.preco_medio, float)
        
    def test_classe_acao_impressao_de_todos_os_attrs(self):
        print(self.acao)


if __name__ == '__main__':
    unittest.main(verbosity=2)
