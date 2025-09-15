from conexao import conectar

class CrudProduto:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def inserir(self, nome, preco, quantidade):
        try:
            sql = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (nome, preco, quantidade))
            self.conn.commit()
            print("✅ Produto inserido com sucesso!")
        except Exception as e:
            print("❌ Erro ao inserir produto:", e)

    def listar_todos(self):
        try:
            self.cursor.execute("SELECT * FROM produtos ORDER BY id")
            produtos = self.cursor.fetchall()
            if produtos:
                print("\n=== LISTA DE PRODUTOS ===")
                for p in produtos:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f} | Quantidade: {p[3]} | Data cadastro: {p[4]}")
            else:
                print("⚠️ Nenhum produto cadastrado.")
        except Exception as e:
            print("❌ Erro ao listar produtos:", e)

    def exibir_um(self, id_produto):
        try:
            self.cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
            p = self.cursor.fetchone()
            if p:
                print(f"\nID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f} | Quantidade: {p[3]} | Data cadastro: {p[4]}")
            else:
                print("⚠️ Produto não encontrado.")
        except Exception as e:
            print("❌ Erro ao exibir produto:", e)

    def pesquisar_por_nome(self, nome):
        try:
            self.cursor.execute("SELECT * FROM produtos WHERE nome ILIKE %s", (f"%{nome}%",))
            produtos = self.cursor.fetchall()
            if produtos:
                print("\n=== RESULTADOS DA PESQUISA ===")
                for p in produtos:
                    print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f} | Quantidade: {p[3]}")
            else:
                print("⚠️ Nenhum produto encontrado.")
        except Exception as e:
            print("❌ Erro ao pesquisar produto:", e)

    def alterar(self, id_produto, nome, preco, quantidade):
        try:
            sql = "UPDATE produtos SET nome=%s, preco=%s, quantidade=%s WHERE id=%s"
            self.cursor.execute(sql, (nome, preco, quantidade, id_produto))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Produto alterado com sucesso!")
            else:
                print("⚠️ Produto não encontrado.")
        except Exception as e:
            print("❌ Erro ao alterar produto:", e)

    def remover(self, id_produto):
        try:
            self.cursor.execute("DELETE FROM produtos WHERE id=%s", (id_produto,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Produto removido com sucesso!")
            else:
                print("⚠️ Produto não encontrado.")
        except Exception as e:
            print("❌ Erro ao remover produto:", e)

    def relatorio(self):
        try:
            #total de produtos
            self.cursor.execute("SELECT COUNT(*) FROM produtos")
            total_produtos = self.cursor.fetchone()[0]
            print(f"\n📊 TOTAL DE PRODUTOS CADASTRADOS: {total_produtos}")

            #menor estoque
            self.cursor.execute("SELECT nome, quantidade FROM produtos ORDER BY quantidade ASC LIMIT 1")
            menor_estoque = self.cursor.fetchone()
            if menor_estoque:
                print(f"📉 Produto com menor estoque: {menor_estoque[0]} ({menor_estoque[1]} unidades)")

            #maior estoque
            self.cursor.execute("SELECT nome, quantidade FROM produtos ORDER BY quantidade DESC LIMIT 1")
            maior_estoque = self.cursor.fetchone()
            if maior_estoque:
                print(f"🔝 Produto com maior estoque: {maior_estoque[0]} ({maior_estoque[1]} unidades)")

            #Valor total do estoque da loja
            self.cursor.execute("SELECT SUM(preco * quantidade) FROM produtos")
            valor_total_estoque = self.cursor.fetchone()[0]
            print(f"💰 Valor total do estoque da loja: R$ {valor_total_estoque:.2f}" if valor_total_estoque else "💰 Valor total do estoque da loja: R$ 0,00")

            #Lista todos os produtos
            self.listar_todos()
        except Exception as e:
            print("❌ Erro ao gerar relatório de produtos:", e)

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
