from conexao import conectar

class CrudVendas:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def registrar_venda(self, cliente_id, produto_id, quantidade):
        try:
            self.cursor.execute("SELECT preco, quantidade FROM produtos WHERE id=%s", (produto_id,))
            resultado = self.cursor.fetchone()
            if not resultado:
                print("⚠️ Produto não encontrado.")
                return
            preco, estoque = resultado
            if quantidade > estoque:
                print("⚠️ Quantidade maior que o estoque disponível.")
                return

            valor_total = preco * quantidade
            self.cursor.execute("INSERT INTO vendas (cliente_id, produto_id, quantidade, valor_total) VALUES (%s, %s, %s, %s)", 
                                (cliente_id, produto_id, quantidade, valor_total))
            self.cursor.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE id=%s", (quantidade, produto_id))
            self.conn.commit()
            print(f"✅ Venda registrada! Valor total: R$ {valor_total:.2f}")
        except Exception as e:
            print("❌ Erro ao registrar venda:", e)

    def listar_todos(self):
        try:
            self.cursor.execute("SELECT * FROM vendas ORDER BY id")
            vendas = self.cursor.fetchall()
            if vendas:
                print("\n=== LISTA DE VENDAS ===")
                for v in vendas:
                    print(f"ID: {v[0]} | Cliente: {v[1]} | Produto: {v[2]} | Quantidade: {v[3]} | Valor total: R$ {v[4]:.2f} | Data: {v[5]}")
            else:
                print("⚠️ Nenhuma venda registrada.")
        except Exception as e:
            print("❌ Erro ao listar vendas:", e)

    def relatorio(self):
        try:
            #vendas totais e valor total vendido
            self.cursor.execute("SELECT COUNT(*), SUM(valor_total) FROM vendas")
            total_vendas, valor_total = self.cursor.fetchone()
            print(f"\n📊 Total de vendas: {total_vendas}")
            print(f"💰 Valor total vendido: R$ {valor_total:.2f}" if valor_total else "💰 Valor total vendido: R$ 0,00")

            # Ticket médio
            ticket_medio = (valor_total / total_vendas) if total_vendas else 0
            print(f"💸 Ticket médio por venda: R$ {ticket_medio:.2f}")

            # Maior venda
            self.cursor.execute("SELECT id, valor_total FROM vendas ORDER BY valor_total DESC LIMIT 1")
            maior_venda = self.cursor.fetchone()
            if maior_venda:
                print(f"🏆 Maior venda: ID {maior_venda[0]} - R$ {maior_venda[1]:.2f}")

            # Produto mais vendido
            self.cursor.execute("SELECT produto_id, SUM(quantidade) as total_qtde FROM vendas GROUP BY produto_id ORDER BY total_qtde DESC LIMIT 1")
            mais_vendido = self.cursor.fetchone()
            if mais_vendido:
                print(f"🛒 Produto mais vendido (em unidades): Produto ID {mais_vendido[0]} - {mais_vendido[1]} unidades")

            # Cliente que mais comprou 
            self.cursor.execute("SELECT cliente_id, SUM(valor_total) FROM vendas GROUP BY cliente_id ORDER BY SUM(valor_total) DESC LIMIT 1")
            top_cliente = self.cursor.fetchone()
            if top_cliente:
                print(f"👑 Cliente que mais comprou: Cliente ID {top_cliente[0]} - Total R$ {top_cliente[1]:.2f}")

            # Lista todas as vendas
            self.listar_todos()
        except Exception as e:
            print("❌ Erro ao gerar relatório de vendas:", e)

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
