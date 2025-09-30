from conexao import conectar

class CrudVendedor:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def inserir(self, nome, cpf=None, matricula=None, email=None, telefone=None, status='ativo'):
        try:
            self.cursor.execute("""
                INSERT INTO vendedor (nome, cpf, matricula, email, telefone, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (nome, cpf, matricula, email, telefone, status))
            vid = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"✅ Vendedor cadastrado! ID: {vid}")
        except Exception as e:
            print("❌ Erro ao inserir vendedor:", e)
            self.conn.rollback()

    def listar_todos(self):
        try:
            self.cursor.execute("""
                SELECT id, nome, cpf, matricula, email, telefone, status, data_admissao, data_demissao
                FROM vendedor
                ORDER BY id
            """)
            rows = self.cursor.fetchall()
            if not rows:
                print("⚠️ Nenhum vendedor cadastrado.")
                return
            print("\n=== LISTA DE VENDEDORES ===")
            for v in rows:
                print(f"ID:{v[0]} | Nome:{v[1]} | CPF:{v[2]} | Matrícula:{v[3]} | Email:{v[4]} | "
                      f"Telefone:{v[5]} | Status:{v[6]} | Admissão:{v[7]} | Demissão:{v[8]}")
        except Exception as e:
            print("❌ Erro ao listar vendedores:", e)

    def alterar(self, vendedor_id, nome=None, email=None, telefone=None, status=None, data_demissao=None):
        try:
            self.cursor.execute("""
                UPDATE vendedor
                   SET nome          = COALESCE(%s, nome),
                       email         = COALESCE(%s, email),
                       telefone      = COALESCE(%s, telefone),
                       status        = COALESCE(%s, status),
                       data_demissao = COALESCE(%s, data_demissao)
                 WHERE id = %s
            """, (nome, email, telefone, status, data_demissao, vendedor_id))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print("✅ Vendedor atualizado!")
            else:
                print("⚠️ Nenhum vendedor com esse ID.")
        except Exception as e:
            print("❌ Erro ao atualizar vendedor:", e)
            self.conn.rollback()

    def remover(self, vendedor_id):
        try:
            self.cursor.execute("DELETE FROM vendedor WHERE id = %s", (vendedor_id,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print("✅ Vendedor removido!")
            else:
                print("⚠️ Nenhum vendedor com esse ID.")
        except Exception as e:
            print("❌ Erro ao remover vendedor:", e)
            self.conn.rollback()

    def __del__(self):
        try:
            if getattr(self, "cursor", None):
                self.cursor.close()
            if getattr(self, "conn", None):
                self.conn.close()
        except:
            pass
