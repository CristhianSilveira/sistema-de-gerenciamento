import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Criar as tabelas no banco
def create_database():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            quantidade INTEGER,
            preco REAL
        )
    ''')

    conn.commit()
    conn.close()


# Cadastrar o usuário no banco
def cadastrar_usuario(nome, sobrenome, email, senha, janela_cadastro):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO usuarios (nome, sobrenome, email, senha)
            VALUES (?, ?, ?, ?)
        ''', (nome, sobrenome, email, senha))
        conn.commit()
        messagebox.showinfo("Cadastro", f"Usuário {nome} {sobrenome} cadastrado com sucesso!")
        janela_cadastro.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "E-mail já cadastrado!")
    finally:
        conn.close()

# Salvar os produtos cadastrado no BD
def salvar_produto(nome, categoria, quantidade, preco, janela):
    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO produtos (nome, categoria, quantidade, preco)
            VALUES (?, ?, ?, ?)
        ''', (nome, categoria, int(quantidade), float(preco)))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Cadastro de Produto", f"Produto '{nome}' cadastrado com sucesso!")
        janela.destroy()

    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preço devem ser números!")
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao cadastrar produto: {e}")


# validação de usuario e senha
def validacao(login, email, senha):
    email = email.get()
    senha = senha.get()

    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        login.destroy()
        janela_gerenciamento()
    else:
        messagebox.showerror("Erro", "Email ou senha inválidos!")


# janela principal
def janela_principal():
    principal = tk.Tk()
    principal.title("Sistema de Gerenciamento")
    principal.geometry("300x200")

    tk.Label(principal, text="Faça login ou se Cadastre!").pack(pady=10)
    tk.Button(principal, text="Login", command=janela_login).pack(pady=10)
    tk.Button(principal, text="Cadastrar", command=janela_cadastro).pack(pady=10)

    principal.mainloop()


# janela de login
def janela_login():
    login = tk.Toplevel()
    login.title("Login")
    login.geometry("300x150")

    tk.Label(login, text="Email:").pack(pady=5)
    email = tk.Entry(login)
    email.pack()

    tk.Label(login, text="Senha:").pack(pady=5)
    senha = tk.Entry(login, show="*")
    senha.pack()

    tk.Button(login, text="Login", command=lambda: validacao(login, email, senha)).pack(pady=10)

    login.mainloop()


# janela de cadastro
def janela_cadastro():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro")
    cadastro.geometry("300x250")

    tk.Label(cadastro, text="Nome:").pack(pady=5)
    nome = tk.Entry(cadastro)
    nome.pack()

    tk.Label(cadastro, text="Sobrenome:").pack(pady=5)
    sobrenome = tk.Entry(cadastro)
    sobrenome.pack()

    tk.Label(cadastro, text="Email:").pack(pady=5)
    email = tk.Entry(cadastro)
    email.pack()

    tk.Label(cadastro, text="Senha:").pack(pady=5)
    senha = tk.Entry(cadastro, show="*")
    senha.pack()

    tk.Button(cadastro, text="Cadastrar", command=lambda: cadastrar_usuario(nome.get(), sobrenome.get(), email.get(), senha.get(), cadastro)).pack(pady=10)

def cadastro_produto():
    cadastro_produto_janela = tk.Toplevel()    
    cadastro_produto_janela.title("Cadastrar Produto")
    cadastro_produto_janela.geometry("300x300")

    tk.Label(cadastro_produto_janela, text="Nome do Produto:").pack(pady=5)
    nome = tk.Entry(cadastro_produto_janela)
    nome.pack()

    tk.Label(cadastro_produto_janela, text="Categoria:").pack(pady=5)
    categoria = tk.Entry(cadastro_produto_janela)
    categoria.pack()

    tk.Label(cadastro_produto_janela, text="Quantidade:").pack(pady=5)
    quantidade = tk.Entry(cadastro_produto_janela)
    quantidade.pack()

    tk.Label(cadastro_produto_janela, text="Preço (R$):").pack(pady=5)
    preco = tk.Entry(cadastro_produto_janela)
    preco.pack()

    def salvar_produto():
        nome = nome.get()
        descricao = descricao.get()
        preco = preco.get()
        quantidade = quantidade.get()

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO produtos (nome, descricao, preco, quantidade)
                VALUES (?, ?, ?, ?)
            ''', (nome, descricao, preco, quantidade))
            conn.commit()

            cursor.execute("SELECT * FROM produtos WHERE rowid = last_insert_rowid()")
            novo_produto = cursor.fetchone()
            tree.insert("", "end", values=novo_produto)

            messagebox.showinfo("Cadastro", f"Produto '{nome}' cadastrado com sucesso!")
            janela_cadastro.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")
        finally:
            conn.close()

    tk.Button(cadastro_produto_janela, text="Cadastrar", command=lambda: salvar_produto(nome.get(), categoria.get(), quantidade.get(), preco.get(), cadastro_produto_janela)).pack(pady=10)

def remover_produto():
    janela_remover = tk.Toplevel()
    janela_remover.title("Remover Produto")
    janela_remover.geometry("300x150")

    tk.Label(janela_remover, text="Digite o ID do produto a ser removido:").pack(pady=10)
    produto_id_entry = tk.Entry(janela_remover)
    produto_id_entry.pack(pady=5)

    def confirmar_remocao():
        produto_id = produto_id_entry.get()

        if not produto_id.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um ID válido.")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if produto:
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Produto com ID {produto_id} removido com sucesso.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

        conn.close()
        janela_remover.destroy()

    tk.Button(janela_remover, text="Remover", command=confirmar_remocao).pack(pady=10)

def editar_produto():
    return


# janela de gerenciamento
def janela_gerenciamento():
    gerenciador = tk.Toplevel()
    gerenciador.title("Sistema de Gerenciamento")
    gerenciador.geometry("500x400")
    tk.Label(gerenciador, text="Bem-vindo ao sistema!").pack(pady=10)

    tk.Label(gerenciador, text="Produtos Cadastrados", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(gerenciador, columns=("ID", "Nome", "Descrição", "Preço", "Quantidade"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Preço", text="Preço")
    tree.heading("Quantidade", text="Quantidade")
    tree.column("ID", width=50)
    tree.column("Nome", width=150)
    tree.column("Descrição", width=200)
    tree.column("Preço", width=80)
    tree.column("Quantidade", width=80)
    tree.pack(pady=10)

    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    for produto in produtos:
        tree.insert("", "end", values=produto)

    tk.Button(gerenciador, text="Cadastrar", command=cadastro_produto).pack(pady=10)
    tk.Button(gerenciador, text="Editar", command=editar_produto).pack(pady=10)
    tk.Button(gerenciador, text="Remover", command=remover_produto).pack(pady=10)
    tk.Button(gerenciador, text="Relatórios", command=janela_relatorio).pack(pady=10)

    gerenciador.mainloop()

# Função para abrir a janela de relatórios
def janela_relatorio():
    relatorio = tk.Toplevel()
    relatorio.title("Relatórios")
    relatorio.geometry("400x300")

    tk.Label(relatorio, text="Relatório de Registros:").pack()
    relatorio.mainloop()


if __name__ == "__main__":
    create_database()
    janela_principal()