import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import webbrowser
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class Banco:
    def __init__(self):
        self.conn = sqlite3.connect('usuarios.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_usuarios (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            usuario TEXT,
            senha TEXT,
            cidade TEXT
        )""")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Usuarios:
    def __init__(self):
        self.banco = Banco()

    def getAllUsers(self):
        self.banco.cursor.execute('SELECT * FROM tbl_usuarios')
        return self.banco.cursor.fetchall()

    def deleteUser(self, usuario_id):
        try:
            self.banco.cursor.execute("DELETE FROM tbl_usuarios WHERE idusuario = ?", (usuario_id,))
            self.banco.conn.commit()
            return "Usuário excluído com sucesso."
        except Exception as e:
            return f"Erro ao excluir usuário: {e}"

class GerenciarUsuarios:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Gerenciar Usuários")
        self.master.geometry("400x400")
        self.fullscreen()

        self.usuario = Usuarios()
        self.lista_usuarios = tk.Listbox(self.master)
        self.lista_usuarios.pack(fill=tk.BOTH, expand=True)

        self.atualizar_lista()

        tk.Button(self.master, text="Fechar", command=self.master.destroy).pack(pady=10)

    def fullscreen(self):
        self.master.attributes("-fullscreen", True)

    def atualizar_lista(self):
        self.lista_usuarios.delete(0, tk.END)
        usuarios_data = self.usuario.getAllUsers()
        for usuario in usuarios_data:
            self.lista_usuarios.insert(tk.END,
                                       f"ID: {usuario[0]:<5} | Nome: {usuario[1]:<20} | Telefone: {usuario[2]:<15} | Email: {usuario[3]:<25} | Cidade: {usuario[6]}")

class PaginaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão")
        self.master.geometry("600x400")
        self.fullscreen()

        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.frame_buttons = tk.Frame(self.frame_top)
        self.frame_buttons.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.criar_botoes()

        tk.Label(self.frame_bottom, text="Banco de Dados", font=("Helvetica", 14)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame_bottom, columns=("ID", "Nome", "Telefone", "Email", "Cidade"),
                                 show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Cidade", text="Cidade")

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.atualizar_lista()

    def fullscreen(self):
        self.master.attributes("-fullscreen", True)

    def criar_botoes(self):
        button_texts = [
            ("Adicionar Usuário", self.adicionar_usuario),
            ("Alterar Usuário", self.alterar_usuario),
            ("Excluir Usuário", self.excluir_usuario),
            ("Gerenciar Usuários", self.gerenciar_usuarios),
            ("Relatório PDF", self.gerar_relatorio),
            ("Carregar Usuários", self.carregar_usuarios),
            ("Sair", self.master.quit)
        ]
        for text, command in button_texts:
            button = tk.Button(self.frame_buttons, text=text, command=lambda cmd=command: self.abrir_tela_cheia(cmd),
                               width=20)
            button.pack(pady=5, padx=5, side=tk.LEFT)

    def carregar_usuarios(self):
        subprocess.Popen(['python', 'app.py'])
        self.master.destroy()

    def abrir_tela_cheia(self, command):
        self.fullscreen()
        command()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        usuarios = Usuarios().getAllUsers()
        for usuario in usuarios:
            self.tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2], usuario[3], usuario[6]))

    def adicionar_usuario(self):
        AdicionarUsuario(self.master)

    def alterar_usuario(self):
        AlterarUsuario(self.master)

    def excluir_usuario(self):
        ExcluirUsuario(self.master)

    def gerenciar_usuarios(self):
        GerenciarUsuarios(self.master)

    def gerar_relatorio(self):
        relatorio = RelatorioPDF(Usuarios())
        relatorio.gerar_relatorio()

# Classes para adicionar, alterar, excluir usuários e gerar relatórios permanecem as mesmas

class AdicionarUsuario:
    # Código da classe AdicionarUsuario
    pass

class AlterarUsuario:
    # Código da classe AlterarUsuario
    pass

class ExcluirUsuario:
    # Código da classe ExcluirUsuario
    pass

class RelatorioPDF:
    # Código da classe RelatorioPDF
    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PaginaPrincipal(root)
    root.mainloop()
