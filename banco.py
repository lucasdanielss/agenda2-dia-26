import sqlite3


class Banco:
    def __init__(self):
        self.conn = sqlite3.connect('usuarios.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabela de usuários
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_usuarios (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            usuario TEXT,
            senha TEXT,
            cidade TEXT
        )""")

        # Tabela de cidades
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_cidades (
            idcidade INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
        )""")

        self.conn.commit()

    def __del__(self):
        self.conn.close()
B