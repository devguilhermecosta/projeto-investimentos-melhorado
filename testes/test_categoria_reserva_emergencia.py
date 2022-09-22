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
from ativos.reserva_emergencia import ReservaEmergencia


class TesteReservaEmergencia(unittest.TestCase):
    def setUp(self) -> None:
        self.re = ReservaEmergencia('CDB Mercado Livre', '15/08/2022', '15/08/2022', '102% CDI')
        
    def test_categoria_reserva_emergencia_attr_valor_aplicado_deve_ser_float(self):
        self.assertIsInstance(self.re.valor_aplicado, float)
    
    def test_categoria_reserva_emergencia_attr_nome_deve_ser_string(self):
        self.assertIsInstance(self.re.nome, str)    

    def test_categoria_reserva_emergencia_attr_quantidade_deve_ser_float(self):
        self.assertIsInstance(self.re.quantidade, float)
        
    def test_categoria_reserva_emergencia_attr_categoria_deve_ser_string(self):
        self.assertIsInstance(self.re.categoria, str)
        
    def test_categoria_reserva_emergencia_attr_carencia_deve_ser_string(self):
        self.assertIsInstance(self.re.resgate, str)
        
    def test_categoria_reserva_emergencia_attr_vencimento_deve_ser_string(self):
        self.assertIsInstance(self.re.vencimento, str)
        
    def test_categoria_reserva_emergencia_attr_rentabilidade_deve_ser_string(self):
        self.assertIsInstance(self.re.rentabilidade, str)
        
    def test_categoria_reserva_emergencia_impressao_geral(self):
        print(self.re)


if __name__ == '__main__':
    unittest.main(verbosity=2)
