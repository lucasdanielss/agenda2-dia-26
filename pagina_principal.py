import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import webbrowser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Banco:
    def __init__(self):
        self.conn = sqlite3.connect('usuarios.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_usuarios (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            usuario TEXT,
            senha TEXT,
            cidade TEXT
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_cidades (
            idcidade INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
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

class Cidades:
    def __init__(self):
        self.banco = Banco()

    def getAllCities(self):
        self.banco.cursor.execute('SELECT * FROM tbl_cidades')
        return self.banco.cursor.fetchall()

class GerenciarUsuarios:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Gerenciar Usuários")
        self.master.geometry("600x400")

        self.usuario = Usuarios()
        self.cidade = Cidades()

        self.tree = ttk.Treeview(self.master, columns=("ID", "Nome", "Telefone", "Email", "Cidade"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Cidade", text="Cidade")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.atualizar_lista()

        tk.Button(self.master, text="Excluir", command=self.excluir_usuario).pack(pady=5)
        tk.Button(self.master, text="Fechar", command=self.fechar).pack(pady=10)

        self.nome_entry = tk.Entry(self.master)
        self.telefone_entry = tk.Entry(self.master)
        self.email_entry = tk.Entry(self.master)
        self.usuario_entry = tk.Entry(self.master)
        self.senha_entry = tk.Entry(self.master, show="*")
        self.cidade_combobox = ttk.Combobox(self.master)

        tk.Label(self.master, text="Nome:").pack(pady=5)
        self.nome_entry.pack(pady=5)
        tk.Label(self.master, text="Telefone:").pack(pady=5)
        self.telefone_entry.pack(pady=5)
        tk.Label(self.master, text="Email:").pack(pady=5)
        self.email_entry.pack(pady=5)
        tk.Label(self.master, text="Usuário:").pack(pady=5)
        self.usuario_entry.pack(pady=5)
        tk.Label(self.master, text="Senha:").pack(pady=5)
        self.senha_entry.pack(pady=5)
        tk.Label(self.master, text="Cidade:").pack(pady=5)
        self.cidade_combobox.pack(pady=5)

        self.load_cidades()

    def load_cidades(self):
        cidades = self.cidade.getAllCities()
        self.cidade_combobox['values'] = [cidade[1] for cidade in cidades]

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')

        # Preencher os campos do formulário com os dados do usuário selecionado
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, values[1])
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, values[2])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[3])
        self.usuario_entry.delete(0, tk.END)
        self.usuario_entry.insert(0, values[4])
        self.senha_entry.delete(0, tk.END)  # Não mostramos a senha por segurança
        self.cidade_combobox.set(values[5])

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        usuarios = self.usuario.getAllUsers()
        for usuario in usuarios:
            self.tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2], usuario[3], usuario[6]))

    def excluir_usuario(self):
        selected_item = self.tree.selection()[0]
        usuario_id = self.tree.item(selected_item, 'values')[0]
        response = self.usuario.deleteUser(usuario_id)
        messagebox.showinfo("Resultado", response)
        self.atualizar_lista()

    def fechar(self):
        self.master.destroy()  # Fecha a janela de gerenciamento

class PaginaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão")
        self.master.geometry("600x400")

        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.frame_buttons = tk.Frame(self.frame_top)
        self.frame_buttons.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.criar_botoes()

        tk.Label(self.frame_bottom, text="Banco de Dados", font=("Helvetica", 14)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame_bottom, columns=("ID", "Nome", "Telefone", "Email", "Cidade"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Cidade", text="Cidade")

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.atualizar_lista()

    def criar_botoes(self):
        button_texts = [
            ("Adicionar Usuário", self.adicionar_usuario),
            ("Gerenciar Usuários", self.gerenciar_usuarios),
            ("Relatório PDF", self.gerar_relatorio),
            ("Carregar Usuários", self.carregar_usuarios),
            ("Sair", self.master.quit)
        ]
        for text, command in button_texts:
            button = tk.Button(self.frame_buttons, text=text, command=command, width=20)
            button.pack(pady=5, padx=5, side=tk.LEFT)

    def carregar_usuarios(self):
        GerenciarUsuarios(self.master)  # Abre a janela de gerenciamento de usuários

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        usuarios = Usuarios().getAllUsers()
        for usuario in usuarios:
            self.tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2], usuario[3], usuario[6]))

    def adicionar_usuario(self):
        AdicionarUsuario(self.master)

    def gerenciar_usuarios(self):
        GerenciarUsuarios(self.master)

    def gerar_relatorio(self):
        relatorio = RelatorioPDF(Usuarios())
        relatorio.gerar_relatorio()

class AdicionarUsuario:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Adicionar Usuário")
        self.master.geometry("400x400")

        self.usuario = Usuarios()
        self.cidade = Cidades()

        tk.Label(self.master, text="Nome:").pack(pady=5)
        self.nome_entry = tk.Entry(self.master)
        self.nome_entry.pack(pady=5)

        tk.Label(self.master, text="Telefone:").pack(pady=5)
        self.telefone_entry = tk.Entry(self.master)
        self.telefone_entry.pack(pady=5)

        tk.Label(self.master, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack(pady=5)

        tk.Label(self.master, text="Usuário:").pack(pady=5)
        self.usuario_entry = tk.Entry(self.master)
        self.usuario_entry.pack(pady=5)

        tk.Label(self.master, text="Senha:").pack(pady=5)
        self.senha_entry = tk.Entry(self.master, show="*")
        self.senha_entry.pack(pady=5)

        tk.Label(self.master, text="Cidade:").pack(pady=5)
        self.cidade_combobox = ttk.Combobox(self.master)
        self.cidade_combobox.pack(pady=5)
        self.load_cidades()

        tk.Button(self.master, text="Salvar", command=self.salvar_usuario).pack(pady=10)
        tk.Button(self.master, text="Voltar", command=self.master.destroy).pack(pady=5)

    def load_cidades(self):
        cidades = self.cidade.getAllCities()
        self.cidade_combobox['values'] = [cidade[1] for cidade in cidades]

    def salvar_usuario(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        cidade = self.cidade_combobox.get()

        try:
            self.usuario.banco.cursor.execute(
                "INSERT INTO tbl_usuarios (nome, telefone, email, usuario, senha, cidade) VALUES (?, ?, ?, ?, ?, ?)",
                (nome, telefone, email, usuario, senha, cidade)
            )
            self.usuario.banco.conn.commit()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar usuário: {e}")

class RelatorioPDF:
    def __init__(self, usuarios):
        self.usuarios = usuarios

    def gerar_relatorio(self):
        pdf_file = "relatorio_usuarios.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100, 750, "Relatório de Usuários")

        usuarios_data = self.usuarios.getAllUsers()
        y = 730
        for usuario in usuarios_data:
            c.drawString(100, y, f"ID: {usuario[0]}, Nome: {usuario[1]}, Telefone: {usuario[2]}, Email: {usuario[3]}, Cidade: {usuario[6]}")
            y -= 20

        c.save()
        messagebox.showinfo("Sucesso", f"Relatório gerado: {pdf_file}")
        webbrowser.open(pdf_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaginaPrincipal(root)
    root.mainloop()
