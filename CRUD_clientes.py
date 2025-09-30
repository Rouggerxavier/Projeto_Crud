from conexao import conectar

class CrudCliente:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def inserir(self, nome, telefone, email, idade, cidade, torce_flamengo=False, assiste_one_piece=False):
        try:
            sql = """
                INSERT INTO clientes (nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece))
            self.conn.commit()
            print("✅ Cliente inserido com sucesso!")
        except Exception as e:
            print("❌ Erro ao inserir cliente:", e)

    def listar_todos(self):
        try:
            sql = "SELECT id, nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece FROM clientes ORDER BY id"
            self.cursor.execute(sql)
            clientes = self.cursor.fetchall()
            if clientes:
                print("\n=== LISTA DE CLIENTES ===")
                for c in clientes:
                    print(f"ID: {c[0]} | Nome: {c[1]} | Telefone: {c[2]} | Email: {c[3]} | Idade: {c[4]} | Cidade: {c[5]} | Flamengo: {c[6]} | One Piece: {c[7]}")
            else:
                print("⚠️ Nenhum cliente cadastrado.")
        except Exception as e:
            print("❌ Erro ao listar clientes:", e)

    def exibir_um(self, id_cliente):
        try:
            sql = "SELECT id, nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece FROM clientes WHERE id = %s"
            self.cursor.execute(sql, (id_cliente,))
            c = self.cursor.fetchone()
            if c:
                print("\n=== DADOS DO CLIENTE ===")
                print(f"ID: {c[0]}")
                print(f"Nome: {c[1]}")
                print(f"Telefone: {c[2]}")
                print(f"Email: {c[3]}")
                print(f"Idade: {c[4]}")
                print(f"Cidade: {c[5]}")
                print(f"Torce Flamengo: {c[6]}")
                print(f"Assiste One Piece: {c[7]}")
            else:
                print("⚠️ Cliente não encontrado.")
        except Exception as e:
            print("❌ Erro ao exibir cliente:", e)

    def alterar(self, id_cliente, nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece):
        try:
            sql = """
                UPDATE clientes 
                SET nome = %s, telefone = %s, email = %s, idade = %s, cidade = %s, torce_flamengo = %s, assiste_one_piece = %s
                WHERE id = %s
            """
            self.cursor.execute(sql, (nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece, id_cliente))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ Cliente alterado com sucesso!")
            else:
                print("⚠️ Cliente não encontrado.")
        except Exception as e:
            print("❌ Erro ao alterar cliente:", e)

    def relatorio(self):
        try:
            self.cursor.execute("SELECT COUNT(*), AVG(idade) FROM clientes")
            total, idade_media = self.cursor.fetchone()
            print(f"\n📊 TOTAL DE CLIENTES: {total}")
            print(f"Média de idade: {idade_media:.2f}" if idade_media else "Média de idade: N/A")
            self.listar_todos()
        except Exception as e:
            print("❌ Erro ao gerar relatório de clientes:", e)

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

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
