from conexao import conectar

class CrudCompra:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def nova_compra(self, cliente_id, vendedor_id):
        """Cria uma compra em aberto"""
        try:
            sql = """
                INSERT INTO compra (cliente_id, vendedor_id, status, status_pagto)
                VALUES (%s, %s, 'aberto', 'pendente')
                RETURNING id
            """
            self.cursor.execute(sql, (cliente_id, vendedor_id))
            compra_id = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"✅ Compra criada! ID: {compra_id}")
            return compra_id
        except Exception as e:
            print("❌ Erro ao criar compra:", e)
            self.conn.rollback()

    def adicionar_item(self, compra_id, produto_id, qtde):
        """Adiciona item à compra"""
        try:
            # Pegar preço do produto
            self.cursor.execute("SELECT preco, quantidade FROM produtos WHERE id = %s", (produto_id,))
            resultado = self.cursor.fetchone()
            if not resultado:
                print("⚠️ Produto não encontrado.")
                return
            preco_unit, estoque = resultado
            if qtde > estoque:
                print("⚠️ Estoque insuficiente.")
                return

            sql = """
                INSERT INTO item_compra (compra_id, produto_id, qtde, preco_unit)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql, (compra_id, produto_id, qtde, preco_unit))
            self.conn.commit()
            print(f"✅ Item adicionado! Produto {produto_id}, Qtde {qtde}, Preço R$ {preco_unit:.2f}")
        except Exception as e:
            print("❌ Erro ao adicionar item:", e)
            self.conn.rollback()

    def finalizar(self, compra_id, forma_pagto_id):
        """Finaliza a compra chamando a Stored Procedure"""
        try:
            self.cursor.execute("CALL finalizar_compra(%s, %s)", (compra_id, forma_pagto_id))
            self.conn.commit()
            print("✅ Compra finalizada com sucesso!")
        except Exception as e:
            print("❌ Erro ao finalizar compra:", e)
            self.conn.rollback()

    def listar_todos(self):
        """Lista todas as compras"""
        try:
            sql = """
                SELECT c.id, c.cliente_id, c.vendedor_id, c.data_compra,
                       c.total_bruto, c.desconto_total, c.total_liquido,
                       c.status, c.status_pagto
                FROM compra c
                ORDER BY c.id
            """
            self.cursor.execute(sql)
            compras = self.cursor.fetchall()
            if compras:
                print("\n=== LISTA DE COMPRAS ===")
                for c in compras:
                    print(f"ID: {c[0]} | Cliente: {c[1]} | Vendedor: {c[2]} | Data: {c[3]} | "
                          f"Bruto: R$ {c[4]:.2f} | Desc: R$ {c[5]:.2f} | Líquido: R$ {c[6]:.2f} | "
                          f"Status: {c[7]} | Pagto: {c[8]}")
            else:
                print("⚠️ Nenhuma compra registrada.")
        except Exception as e:
            print("❌ Erro ao listar compras:", e)

    def relatorio(self):
        """Relatório de compras"""
        try:
            # Totais
            self.cursor.execute("SELECT COUNT(*), SUM(total_liquido) FROM compra WHERE status = 'pago'")
            total, valor = self.cursor.fetchone()
            print(f"\n📊 Compras finalizadas: {total}")
            print(f"💰 Valor total vendido: R$ {valor:.2f}" if valor else "💰 Valor total vendido: R$ 0,00")

            # Maior compra
            self.cursor.execute("SELECT id, total_liquido FROM compra ORDER BY total_liquido DESC LIMIT 1")
            maior = self.cursor.fetchone()
            if maior:
                print(f"🏆 Maior compra: ID {maior[0]} - R$ {maior[1]:.2f}")

            # Cliente destaque
            self.cursor.execute("""
                SELECT cliente_id, SUM(total_liquido)
                FROM compra
                GROUP BY cliente_id
                ORDER BY SUM(total_liquido) DESC LIMIT 1
            """)
            cliente = self.cursor.fetchone()
            if cliente:
                print(f"👑 Cliente que mais comprou: ID {cliente[0]} - R$ {cliente[1]:.2f}")

            # Vendedor destaque
            self.cursor.execute("""
                SELECT vendedor_id, SUM(total_liquido)
                FROM compra
                GROUP BY vendedor_id
                ORDER BY SUM(total_liquido) DESC LIMIT 1
            """)
            vendedor = self.cursor.fetchone()
            if vendedor:
                print(f"⭐ Vendedor destaque: ID {vendedor[0]} - R$ {vendedor[1]:.2f}")

            self.listar_todos()
        except Exception as e:
            print("❌ Erro ao gerar relatório de compras:", e)

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
