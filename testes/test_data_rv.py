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
from modulos.ativos.acoes import Acao
from modulos.ativos.fiis import Fiis
from data.data import RepositorioRendaVariavel
from data.exceptions import AtivoJaCadastradoError, AtivoNaoCadastradoError, QuantidadeInsuficienteError
import random as rd


class TestBancoDadosRv(unittest.TestCase):
    def setUp(self) -> None:
        self.rep: RepositorioRendaVariavel = RepositorioRendaVariavel()
        
    def test_bd_connection_ok_deve_retorna_0(self):
        self.assertEqual(self.rep._conn.total_changes, 0)
        
    def test_bd_func_cadastrar_ativo_retorna_ativojacadastradoerror_se_ativo_ja_existir(self):
        ativo = Fiis('Teste', 'TTSE3')
        with self.assertRaises(AtivoJaCadastradoError):
            self.rep.cadastrar_ativo(ativo)
            
    def test_bd_func_cadastrar_ativo_retorna_zero_se_ativo_se_cadastrado(self):
        ativo_ficticio = self.gerar_ativo()
        ativo = Fiis(ativo_ficticio[0], ativo_ficticio[1])
        self.assertEqual(self.rep.cadastrar_ativo(ativo), 0)
        
    def test_bd_func_get_id_deve_retornar_negativo_1_se_ativo_nao_encontrado(self):
        ativo = Acao('Teste', '1234')
        self.assertEqual(self.rep._get_id_rv(ativo.codigo), -1)
            
    def test_bd_func_get_id_deve_retornar_o_id_se_ativo_encontrado(self):
        ativo = Acao('Banco', 'BBAS3') # o id é 2
        self.assertEqual(self.rep._get_id_rv(ativo.codigo), 2)
        
    def test_bd_func_comprar_deve_retornar_ativonaocadastradoerror_se_ativo_nao_cadastrado_ainda(self):
        ativo_ficticio = self.gerar_ativo()
        ativo = Acao(ativo_ficticio[0], ativo_ficticio[1])
        
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.comprar(ativo, 1, 1.0)
            
    def test_bd_func_comprar_deve_retornar_0_se_compra_concluida_com_sucesso(self):
        ativo = Acao('Teste', 'TTSE3')
        self.assertEqual(self.rep.comprar(ativo, 1, 2.50), 0)
        
    def test_bd_func_vender_deve_retornar_0_se_venda_concluida_com_sucesso(self):
        ativo = Acao('Banco', 'BBAS3')
        self.assertEqual(self.rep.vender(ativo, 1, 28.29), 0)
        
    def test_bd_func_vender_deve_retornar_quantidade_insuficiente_se_ativo_nao_tiver_quantidade_para_venda(self):
        ativo = Acao('Sanepar', 'SANP4')
        with self.assertRaises(QuantidadeInsuficienteError):
            self.rep.vender(ativo, 1, 2.50)
    
    def test_bd_func_qtde_disponivel_deve_retornar_true_se_maior_que_zero(self):
        ativo = Acao('Gerdau', 'GGDR4')
        self.assertTrue(self.rep._quantidade_suficiente(ativo))
        
    def test_bd_func_qtde_disponivel_deve_retornar_false_se_menor_ou_igual_a_zero(self):
        ativo = Acao('Sanepar', 'SANP4')
        self.assertFalse(self.rep._quantidade_suficiente(ativo))
        
    def test_bd_func_deletar_ativo_deve_retornar_0_se_ativo_deletado(self):
        ativo = self.ativo_qualquer_para_ser_deletado()
        self.assertEqual(self.rep.deletar(ativo), 0)
        
    def test_bd_func_alterar_dados_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo = Acao('BTG Pactual', '***')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.alterar_dados(ativo, 'BTG Pactual', 'BTLG11')
        
    def test_bd_func_alterar_dados_deve_retornar_0_se_alteracoes_concluidas(self):
        ativo = Acao('BTG Pactual', 'BTLG11')
        self.assertEqual(self.rep.alterar_dados(ativo, 'BTG Pactual', 'BTLG11'), 0)

    def test_bd_func_acertar_quantidade_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo = Fiis('DCAz0Wur', '**')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.acertar_quantidade(ativo, 1)
          
    def test_bd_func_acertar_quantidade_deve_retornar_0_se_acertado(self):
        ativo = Fiis('DCAz0Wur', 'gjhk')
        self.assertEqual(self.rep.acertar_quantidade(ativo, 10), 0)

    def test_bd_func_acertar_preco_unitario_deve_retornar_ativonaocadastradoerror_se_ativo_nao_existir(self):
        ativo = Acao('BTG Pactual', '**')
        with self.assertRaises(AtivoNaoCadastradoError):
            self.rep.acertar_preco_unit(ativo, 21.50)

    def test_bd_func_acertar_preco_unitario_deve_retornar_0_se_acertado(self):
        ativo = Acao('BTG Pactual', 'BTLG11')
        self.assertEqual(self.rep.acertar_preco_unit(ativo, 93.20), 0)
        
    @staticmethod
    def gerar_ativo() -> tuple:
        """
        Gera um ativo fictício para os testes.
        
        Retorna uma tupla contendo um NOME (indice 0) e um CÓDIGO (indice 1).
        """
        lp: str = 'abcdefghijklmnopqrstuvxywz'
        lg: str = lp.upper()
        num: str = '0123456789'
        
        caracteres: str = (lp + lg + num)
        nome: str = "".join(rd.sample(caracteres, 8))
        codigo: str = "".join(rd.sample(caracteres, 4))
        
        ativo: tuple = (nome, codigo)
        
        return ativo
    
    def ativo_qualquer_para_ser_deletado(self) -> Acao:
        """
        Retorna um objeto do tipo Acao existente dentro do banco de dados.
        Trata-se de um objeto com quantidade igual a zero para não
        afetar os demais testes.
        Este ativo será deletado assim que instanciado.
        """
        acao: str = "SELECT * FROM RV"
        self.rep._cursor.execute(acao)
        
        for at in self.rep._cursor.fetchall():
            if at[4] == 0 and at[2] != 'SANP4' and at[2] != 'BTLG11':
                ativo = at
                break
        return Acao(ativo[1], ativo[2])
        
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
