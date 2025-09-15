import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            dbname="Projeto_Crud",
            user="postgres",
            password="Rougg1327",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Erro na conexão:", e)
        return None
