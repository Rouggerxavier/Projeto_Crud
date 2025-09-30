from conexao import conectar

class CrudProduto:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def inserir(self, nome, preco, quantidade, tipo=None, origem_cidade=None):
        try:
            sql = """
                INSERT INTO produtos (nome, preco, quantidade, tipo, origem_cidade)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (nome, preco, quantidade, tipo, origem_cidade))
            self.conn.commit()
            print("✅ Produto inserido com sucesso!")
        except Exception as e:
            print("❌ Erro ao inserir produto:", e)

    def listar_todos(self):
        try:
            sql = "SELECT id, nome, preco, quantidade, data_cadastro, tipo, origem_cidade FROM produtos ORDER BY id"
            self.cursor.execute(sql)
            produtos = self.cursor.fetchall()
            if produtos:
                print("\n=== LISTA DE PRODUTOS ===")
                for p in produtos:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f} | Qtde: {p[3]} | Data: {p[4]} | Tipo: {p[5]} | Origem: {p[6]}")
            else:
                print("⚠️ Nenhum produto cadastrado.")
        except Exception as e:
            print("❌ Erro ao listar produtos:", e)

    def exibir_um(self, id_produto):
        try:
            sql = "SELECT id, nome, preco, quantidade, data_cadastro, tipo, origem_cidade FROM produtos WHERE id = %s"
            self.cursor.execute(sql, (id_produto,))
            p = self.cursor.fetchone()
            if p:
                print("\n=== DADOS DO PRODUTO ===")
                print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f} | Qtde: {p[3]} | Data: {p[4]} | Tipo: {p[5]} | Origem: {p[6]}")
            else:
                print("⚠️ Produto não encontrado.")
        except Exception as e:
            print("❌ Erro ao exibir produto:", e)

    def pesquisar_por_nome(self, nome):
        try:
            sql = "SELECT id, nome, preco, quantidade, tipo, origem_cidade FROM produtos WHERE nome ILIKE %s"
            self.cursor.execute(sql, (f"%{nome}%",))
            produtos = self.cursor.fetchall()
            if produtos:
                print("\n=== RESULTADOS DA PESQUISA ===")
                for p in produtos:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f} | Qtde: {p[3]} | Tipo: {p[4]} | Origem: {p[5]}")
            else:
                print("⚠️ Nenhum produto encontrado.")
        except Exception as e:
            print("❌ Erro ao pesquisar produto:", e)

    def alterar(self, id_produto, nome, preco, quantidade, tipo=None, origem_cidade=None):
        try:
            sql = """
                UPDATE produtos
                SET nome=%s, preco=%s, quantidade=%s, tipo=%s, origem_cidade=%s
                WHERE id=%s
            """
            self.cursor.execute(sql, (nome, preco, quantidade, tipo, origem_cidade, id_produto))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Produto alterado com sucesso!")
            else:
                print("⚠️ Produto não encontrado.")
        except Exception as e:
            print("❌ Erro ao alterar produto:", e)

    def remover(self, id_produto):
        try:
            sql = "DELETE FROM produtos WHERE id=%s"
            self.cursor.execute(sql, (id_produto,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Produto removido com sucesso!")
            else:
                print("⚠️ Produto não encontrado.")
        except Exception as e:
            print("❌ Erro ao remover produto:", e)

    def relatorio(self):
        try:
            # total de produtos
            self.cursor.execute("SELECT COUNT(*) FROM produtos")
            total = self.cursor.fetchone()[0]
            print(f"\n📊 TOTAL DE PRODUTOS: {total}")

            # menor estoque
            self.cursor.execute("SELECT nome, quantidade FROM produtos ORDER BY quantidade ASC LIMIT 1")
            menor = self.cursor.fetchone()
            if menor:
                print(f"📉 Menor estoque: {menor[0]} ({menor[1]} unidades)")

            # maior estoque
            self.cursor.execute("SELECT nome, quantidade FROM produtos ORDER BY quantidade DESC LIMIT 1")
            maior = self.cursor.fetchone()
            if maior:
                print(f"🔝 Maior estoque: {maior[0]} ({maior[1]} unidades)")

            # valor total em estoque
            self.cursor.execute("SELECT SUM(preco * quantidade) FROM produtos")
            valor = self.cursor.fetchone()[0]
            print(f"💰 Valor total em estoque: R$ {valor:.2f}" if valor else "💰 Valor total em estoque: R$ 0,00")

            # lista todos
            self.listar_todos()
        except Exception as e:
            print("❌ Erro ao gerar relatório de produtos:", e)

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
