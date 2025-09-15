from conexao import conectar

class CrudCliente:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def inserir(self, nome, telefone, email, idade):
        try:
            sql = "INSERT INTO clientes (nome, telefone, email, idade) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (nome, telefone, email, idade))
            self.conn.commit()
            print("✅ Cliente inserido com sucesso!")
        except Exception as e:
            print("❌ Erro ao inserir cliente:", e)

    def listar_todos(self):
        try:
            self.cursor.execute("SELECT * FROM clientes ORDER BY id")
            clientes = self.cursor.fetchall()
            if clientes:
                print("\n=== LISTA DE CLIENTES ===")
                for cliente in clientes:
                    print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Telefone: {cliente[2]} | Email: {cliente[3]} | Idade: {cliente[5]}")
            else:
                print("⚠️ Nenhum cliente cadastrado.")
        except Exception as e:
            print("❌ Erro ao listar clientes:", e)

    def exibir_um(self, id_cliente):
        try:
            self.cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
            cliente = self.cursor.fetchone()
            if cliente:
                print("\n=== DADOS DO CLIENTE ===")
                print(f"ID: {cliente[0]}")
                print(f"Nome: {cliente[1]}")
                print(f"Telefone: {cliente[2]}")
                print(f"Email: {cliente[3]}")
                print(f"Data cadastro: {cliente[4]}")
                print(f"Idade: {cliente[5]}")
            else:
                print("⚠️ Cliente não encontrado.")
        except Exception as e:
            print("❌ Erro ao exibir cliente:", e)

    def pesquisar_por_nome(self, nome):
        try:
            sql = "SELECT * FROM clientes WHERE nome ILIKE %s"
            self.cursor.execute(sql, (f"%{nome}%",))
            clientes = self.cursor.fetchall()
            if clientes:
                print("\n=== RESULTADOS DA PESQUISA ===")
                for cliente in clientes:
                    print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Telefone: {cliente[2]} | Email: {cliente[3]} | Idade: {cliente[5]}")
            else:
                print("⚠️ Nenhum cliente encontrado com esse nome.")
        except Exception as e:
            print("❌ Erro ao pesquisar cliente:", e)

    def alterar(self, id_cliente, nome, telefone, email, idade):
        try:
            sql = "UPDATE clientes SET nome = %s, telefone = %s, email = %s, idade = %s WHERE id = %s"
            self.cursor.execute(sql, (nome, telefone, email, idade, id_cliente))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Cliente alterado com sucesso!")
            else:
                print("⚠️ Cliente não encontrado.")
        except Exception as e:
            print("❌ Erro ao alterar cliente:", e)

    def remover(self, id_cliente):
        try:
            sql = "DELETE FROM clientes WHERE id = %s"
            self.cursor.execute(sql, (id_cliente,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Cliente removido com sucesso!")
            else:
                print("⚠️ Cliente não encontrado.")
        except Exception as e:
            print("❌ Erro ao remover cliente:", e)

    def relatorio(self):
        try:
            #total de clientes e idade média
            self.cursor.execute("SELECT COUNT(*), AVG(idade) FROM clientes")
            total, idade_media = self.cursor.fetchone()
            
            #número total de clientes
            print(f"\n📊 TOTAL DE CLIENTES CADASTRADOS: {total}")
            
            # Relatório idade média
            print("\n=== RELATÓRIO DE CLIENTES ===")
            print(f"Média de idade: {idade_media:.2f}" if idade_media else "Média de idade: N/A")
            
            # Lista todos os clientes
            self.listar_todos()
        except Exception as e:
            print("❌ Erro ao gerar relatório de clientes:", e)

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
