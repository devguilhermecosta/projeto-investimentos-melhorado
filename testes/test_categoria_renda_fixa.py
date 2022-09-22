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
from ativos.renda_fixa import RendaFixa


class TesteReservaRendaFixa(unittest.TestCase):
    def setUp(self):
        self.rf = RendaFixa('CDB BTG Pactual', 'imediata', '15/08/2022', '102% CDI')

    def test_categoria_renda_fixa_attr_valor_aplicado_deve_ser_float(self):
        self.assertIsInstance(self.rf.valor_aplicado, float)

    def test_categoria_renda_fixa_attr_nome_deve_ser_string(self):
        self.assertIsInstance(self.rf.nome, str)
       
    def test_categoria_renda_fixa_attr_categoria_deve_ser_string(self):
        self.assertIsInstance(self.rf.categoria, str)
  
    def test_categoria_renda_fixa_attr_carencia_deve_ser_string(self):
        self.assertIsInstance(self.rf.resgate, str)
   
    def test_categoria_renda_fixa_attr_vencimento_deve_ser_string(self):
        self.assertIsInstance(self.rf.vencimento, str)
 
    def test_categoria_renda_fixa_attr_rentabilidade_deve_ser_string(self):
        self.assertIsInstance(self.rf.rentabilidade, str)

    def test_categoria_renda_fixa_impressao_geral(self):
        print(self.rf)


if __name__ == '__main__':
    unittest.main(verbosity=2)