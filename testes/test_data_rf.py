try:
    import sys
    import os
    
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../'
            )
        )
    )
except Exception as error:
    print(f'{error}')
    
import unittest
from data.exceptions import AtivoJaCadastradoError, AtivoNaoCadastradoError, SaldoInsuficienteError
from modulos.ativos.renda_fixa import RendaFixa
from modulos.ativos.reserva_emergencia import ReservaEmergencia
from data.data import RepositorioRendaFixa
import unittest
import random as rd


class TestBancoDadosRF(unittest.TestCase):
    def setUp(self):
        self.rep = RepositorioRendaFixa()
        
    def test_bd_conexao_com_banco_de_dados_deve_retornar_0_se_conectado(self):
        self.assertEqual(self.rep._conn.total_changes, 0)
        
    def test_bd_func_get_id_deve_retornar_int(self):
        ativo: RendaFixa = RendaFixa('CDB', '21/02/2023', '21/02/2023', '103% CDI')
        self.assertIsInstance(self.rep._get_id(ativo), int)
        
    def test_bd_func_get_id_deve_retornar_negativo_um_se_ativo_nao_existir(self):
        ativo: RendaFixa = RendaFixa('Não Existe', '21/02/2023', '21/02/2023', '103% CDI')
        self.assertEqual(self.rep._get_id(ativo), -1)
        
    def test_bd_func_get_id_deve_retornar_int_maior_que_zero_se_ativo_existir(self):
        ativo: RendaFixa = RendaFixa('CDB', '21/02/2023', '21/02/2023', '102% CDI')
        self.assertNotEqual(self.rep._get_id(ativo), -1)
        
    def test_bd_func_existe_deve_retornar_false_se_ativo_nao_existir(self):
        ativo: RendaFixa = RendaFixa('Não Existe', '21/02/2023', '21/02/2023', '103% CDI')
        self.assertFalse(self.rep._existe(ativo))
        
    def test_bd_func_existe_deve_retornar_true_se_ativo_existir(self):
        ativo: RendaFixa = RendaFixa('CDB', '21/02/2023', '21/02/2023', '103% CDI')
        self.assertTrue(self.rep._existe(ativo))
        
    def test_bd_func_cadastrar_ativo_deve_retornar_ativojacadastradoerror_se_ja_existir(self):
        ativo: RendaFixa = RendaFixa('CDB', '21/02/2023', '21/02/2023', '103% CDI')
        with self.assertRaises(AtivoJaCadastradoError):
            self.rep.cadastrar_ativo(ativo)
            
    def test_bd_func_cadastrar_ativo_deve_retornar_zero_se_ativo_cadastrado_com_sucesso(self):
        ativo_ficticio: tuple = self.gerar_ativo()
        ativo: RendaFixa = RendaFixa(ativo_ficticio[0], ativo_ficticio[1], ativo_ficticio[2], ativo_ficticio[3])
        self.assertEqual(self.rep.cadastrar_ativo(ativo), 0)
        
    def test_bd_func_comprar_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo: ReservaEmergencia = ReservaEmergencia('CDB 123', 'Imediato', '31/12/2022', '101% CDI')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.comprar(ativo, 1, 147.50)
            
    def test_bd_func_comprar_deve_retornar_zero_se_ativo_comprado_com_sucesso(self):
        ativo: RendaFixa = RendaFixa('CDB', '21/02/2023', '21/02/2023', '103% CDI')
        self.assertEqual(self.rep.comprar(ativo, 1, 1), 0)
    
    def test_bd_func_resgatar_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo: RendaFixa = RendaFixa('Não Existe', '21/02/2023', '21/02/2023', '103% CDI')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.resgatar(ativo, 1, 100.0)  
        
    def test_bd_func_resgatar_deve_retornar_saldoinsuficienteerror_se_saldo_menor_ou_igual_a_zero(self):
        ativo: RendaFixa = RendaFixa('Teste', '21/02/2023', '21/02/2023', '102% CDI')        
        with self.assertRaises(SaldoInsuficienteError):
            self.rep.resgatar(ativo, 1, 100.0)
    
    def test_bd_func_resgatar_deve_retornar_zero_se_resgate_concluido(self):
        ativo: RendaFixa = RendaFixa('CDB', '21/02/2023', '21/02/2023', '103% CDI')
        self.assertEqual(self.rep.resgatar(ativo, 1, 100), 0)
        
    def test_bd_func_alterar_dados_ativo_deve_retornar_zero_se_data_alterada_com_sucesso(self):
        ativo: RendaFixa = RendaFixa('Novo Nome', '10/02/2023', '10/02/2023', '110% CDI')
        self.assertEqual(self.rep.alterar_dados_ativo(ativo, 'Novo Nome', '30/08/2022', '30/08/2022', '15% a.a'), 0)
        
    def test_bd_func_alterar_dados_ativo_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo: RendaFixa = RendaFixa('Não Existe', '30/08/2023', '30/08/2023', '101% CDI')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.alterar_dados_ativo(ativo, 'Não Existe', '01/01/2024', '01/01/2024', '102% CDI')
            
    def test_bd_func_acertar_valor_aplicado_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo: RendaFixa = RendaFixa('Não Existe', '30/08/2023', '30/08/2023', '101% CDI')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.acertar_valor_aplicado(ativo, 1589.50)
    
    def test_bd_func_acertar_valor_aplicado_deve_retornar_zero_se_ativo_alterado_com_sucesso(self):
        ativo: RendaFixa = RendaFixa('Novo Nome', '10/02/2023', '10/02/2023', '110% CDI')
        self.assertEqual(self.rep.acertar_valor_aplicado(ativo, 25850.59), 0)
        
    def test_bd_func_deletar_ativo_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo: RendaFixa = RendaFixa('Não Existe', '30/08/2023', '30/08/2023', '101% CDI')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.deletar_ativo(ativo)
            
    def test_bd_func_deletar_ativo_deve_retornar_zero_se_ativo_deletado_com_sucesso(self):
        ativo: RendaFixa = self.ativo_qualquer_para_ser_deletado()
        self.assertEqual(self.rep.deletar_ativo(ativo), 0)
    
    def test_bd_func_relatorio_reserva_emergencia_deve_retornar_int_ou_float(self):
        self.assertIsInstance(self.rep.relatorio_res_emerg(), int | float)
    
    def test_bd_func_relatorio_tesouro_diretori_deve_retornar_int_ou_float(self):
        self.assertIsInstance(self.rep.relatorio_tesouro_direto(), int | float)

    def test_bd_func_relatorio_renda_fixa_deve_retornar_int_ou_float(self):
        self.assertIsInstance(self.rep.relatorio_renda_fixa(), int | float)
        
            
    @staticmethod            
    def gerar_ativo():
        lp: str = 'abcdefghijklmnopqrstuvxywz'
        lg: str = lp.upper()
        num: str = '0123456789'
        
        resgate: tuple = ('Imediato', '31/12/2022', '10/02/2023', '04/07/2024')
        vencimento: tuple = ('10/11/2022', '31/12/2022', '10/02/2023', '04/07/2024')
        rentabilidade: tuple = ('101% CDI', '102% CDI', '103% CDI', '110% CDI')
        
        caracteres: str = (lp + lg + num)
        nome: str = "".join(rd.sample(caracteres, 8))
        resgat: str = rd.choice(resgate)
        vencim: str = rd.choice(vencimento)
        rent: str = rd.choice(rentabilidade)
        
        ativo: tuple = (nome, resgat, vencim, rent)
        
        return ativo
    
    def ativo_qualquer_para_ser_deletado(self) -> RendaFixa:
        """
        Retorna um objeto existente dentro do banco de dados.
        Trata-se de um objeto com quantidade igual a zero para não
        afetar os demais testes.
        Este ativo será deletado assim que instanciado.
        """
        acao: str = "SELECT * FROM RF"
        self.rep._cursor.execute(acao)
        
        for at in self.rep._cursor.fetchall():
            lista: tuple = ('CDB', 'Teste', 'CDB BB', 'Novo Nome')
            for l in lista:
                if at[1] != l:
                    ativo = at
                    break
        return RendaFixa(ativo[1], ativo[4], ativo[6], ativo[7])


if __name__ == '__main__':
    unittest.main(verbosity=2)
