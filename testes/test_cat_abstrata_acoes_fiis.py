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
from abc import ABC
from ativos.ativo import AtivoAcoesFiis


class TesteAtivo(unittest.TestCase):
    def setUp(self):
        self.ativo = AtivoAcoesFiis('Teste', 'TTR4F', 'Ações')

    def test_ativo_deve_ser_uma_instancia_abstrata(self):
        self.assertIsInstance(self.ativo, ABC)

    def test_ativo_attr_nome_deve_ser_uma_string(self):
        self.assertIsInstance(self.ativo.nome, str)

    def test_ativo_attr_codigo_deve_ser_uma_string(self):
        self.assertIsInstance(self.ativo.codigo, str)

    def test_ativo_attr_categoria_deve_ser_string(self):
        self.assertIsInstance(self.ativo.categoria, str)

    def test_ativo_attr_quantidade_deve_ser_inteiro(self):
        self.assertIsInstance(self.ativo.quantidade, int)

    def test_ativo_preco_unitario_deve_ser_float(self):
        self.assertIsInstance(self.ativo.preco_unitario, float)

    def test_ativo_preco_medio_deve_ser_float(self):
        self.assertIsInstance(self.ativo.preco_medio, float)


if __name__ == '__main__':
    unittest.main(verbosity=2)
