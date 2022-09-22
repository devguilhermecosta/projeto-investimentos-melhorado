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

from time import strftime
import unittest
from ativos.tesouro_direto import TesouroDireto
from datetime import datetime


class TesteCategoriaTesoutoDireto(unittest.TestCase):

    data_atual = datetime.now().strftime('%d/%m/%Y')
    
    def setUp(self):
        self.td = TesouroDireto('CDB BTG Pactual', 
                                '15/08/2022', 
                                '15/08/2022',
                                '102% CDI',
                                'Fevereiro e Março',
                                )
        
    def test_categoria_tesouro_direto_attr_nome_deve_ser_string(self):
        self.assertIsInstance(self.td.nome, str)
        
    def test_categoria_tesouro_direto_attr_carencia_deve_ser_string(self):
        self.assertIsInstance(self.td.resgate, str)
        
    def test_categoria_tesouro_direto_attr_carencia_deve_ter_formato_dd_mm_aa(self):
        self.assertEqual(self.td.resgate, TesteCategoriaTesoutoDireto.data_atual)
        
    def test_categoria_tesouro_direto_attr_vencimento_deve_ser_string(self):
        self.assertIsInstance(self.td.vencimento, str)
        
    def test_categoria_tesouro_direto_attr_vencimento_deve_ter_formato_dd_mm_aa(self):
        self.assertEqual(self.td.vencimento, TesteCategoriaTesoutoDireto.data_atual)
        
    def test_categoria_tesouro_direto_attr_periodicidade_pagamentos_deve_ser_string(self):
        self.assertIsInstance(self.td.periodicidade_pagamentos, str)
        
    def test_categoria_tesouro_direto_print_de_todos_os_atributos(self):
        print(self.td)
        


if __name__ == '__main__':
    unittest.main(verbosity=2)
