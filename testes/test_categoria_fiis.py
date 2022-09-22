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
from ativos.fiis import Fiis


class TesteCategoriaFiis(unittest.TestCase):
    def setUp(self):
        self.fii = Fiis('Maxima Renda FII', 'MXRF11')

    def test_classe_fii_attr_nome_deve_ser_string(self):
        self.assertIsInstance(self.fii.nome, str)

    def test_classe_fii_attr_codigo_deve_ser_string(self):
        self.assertIsInstance(self.fii.codigo, str)

    def test_classe_fii_attr_categoria_deve_ser_string(self):
        self.assertIsInstance(self.fii.categoria, str)

    def test_classe_fii_attr_quantidade_deve_ser_int(self):
        self.assertIsInstance(self.fii.quantidade, int)  

    def test_classe_fii_attr_preco_unitario_deve_ser_float(self):
        self.assertIsInstance(self.fii.preco_unitario, float)

    def test_classe_fii_attr_preco_medio_deve_ser_float(self):
        self.assertIsInstance(self.fii.preco_medio, float)

    def test_classe_fii_impressao_de_todos_os_attrs(self):
        print(self.fii)


if __name__ == '__main__':
    unittest.main(verbosity=2)
