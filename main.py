import tkinter as tk
import csv
import sqlite3
import backend as backend
from tkinter import ttk, messagebox, filedialog


# Volta para a janela anterior
def voltar_janela(janela_atual, janela_anterior):
    if janela_atual:
        janela_atual.withdraw() # Oculta a janela atual
    janela_anterior.deiconify()


# Janela principal do app
def janela_principal():
    principal = tk.Tk()
    principal.title("Sistema de Gerenciamento de Produtos")
    principal.geometry("400x200")

    tk.Label(principal, text="Faça login ou se Cadastre!", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(principal, text="Login", command=lambda: janela_login(principal), bg="#007acc", fg="#ffffff", font=("Helvetica", 12), width=15,).pack(pady=20)
    tk.Button(principal, text="Cadastro", command=lambda: janela_cadastro(principal), bg="#006022", fg="#ffffff", font=("Helvetica", 12), width=15,).pack(pady=10)

    principal.mainloop()


# janela de login
def janela_login(principal):
    principal.withdraw()
    login = tk.Toplevel()
    login.title("Login")
    login.geometry("400x300")

    tk.Label(login, text="Entre no sistema!", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=15)

    tk.Label(login, text="Email:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    email = tk.Entry(login, width=30)
    email.pack()

    tk.Label(login, text="Senha:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    senha = tk.Entry(login, show="*", width=30)
    senha.pack()

    botoes_frame = tk.Frame(login)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Login", command=lambda: backend.validacao_login(login, email, senha), bg="#330088", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=0, padx=10, pady=20)
    tk.Button(botoes_frame, text="Voltar", command=lambda: voltar_janela(login, principal), bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=1, padx=10, pady=20)


# janela de cadastro
def janela_cadastro(principal):
    principal.withdraw()
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro")
    cadastro.geometry("400x400")

    tk.Label(cadastro, text="Insira seus Dados!", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=15)

    tk.Label(cadastro, text="Nome:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    nome = tk.Entry(cadastro, width=30)
    nome.pack()

    tk.Label(cadastro, text="Sobrenome:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    sobrenome = tk.Entry(cadastro, width=30)
    sobrenome.pack()

    tk.Label(cadastro, text="Email:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    email = tk.Entry(cadastro, width=30)
    email.pack()

    tk.Label(cadastro, text="Senha:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    senha = tk.Entry(cadastro, show="*", width=30)
    senha.pack()

    botoes_frame = tk.Frame(cadastro)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Cadastrar", command=lambda: backend.cadastrar_usuario(nome.get(), sobrenome.get(), email.get(), senha.get(), cadastro), bg="#330088", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=0, padx=10, pady=20)
    tk.Button(botoes_frame, text="Voltar", command=lambda: voltar_janela(cadastro, principal), bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=1, padx=10, pady=20)


# Janela de cadastrar produto e salvar o produto no BD
def janela_cadastro_produto(visor, gerenciador):
    cadastro_produto = tk.Toplevel()    
    cadastro_produto.title("Cadastrar Produto")
    cadastro_produto.geometry("400x400")

    tk.Label(cadastro_produto, text="Insira os dados do Produtos", bg="#f0f0f0", font=("Helvetica", 16)).pack(pady=5)

    tk.Label(cadastro_produto, text="Nome do Produto:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    nome_produto = tk.Entry(cadastro_produto, width=30)
    nome_produto.pack()

    tk.Label(cadastro_produto, text="Categoria:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    categoria = tk.Entry(cadastro_produto, width=30)
    categoria.pack()

    tk.Label(cadastro_produto, text="Quantidade:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    quantidade = tk.Entry(cadastro_produto, width=30)
    quantidade.pack()

    tk.Label(cadastro_produto, text="Preço (R$):", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    preco = tk.Entry(cadastro_produto, width=30)
    preco.pack()

    botoes_frame = tk.Frame(cadastro_produto)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar", command=lambda: backend.salvar_produto(nome_produto, categoria, quantidade, preco, cadastro_produto, visor), bg="#005500", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=0, padx=10, pady=20)
    tk.Button(botoes_frame, text="Cancelar", command=lambda: voltar_janela(cadastro_produto, gerenciador), bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=1, padx=10, pady=20)


# Janela de remover produto do BD
def janela_remover_produto(visor, gerenciador):
    remover = tk.Toplevel()
    remover.title("Remover Produto")
    remover.geometry("400x200")

    tk.Label(remover, text="Digite o ID do produto a ser removido:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    produto = tk.Entry(remover, width=30)
    produto.pack(pady=5)
        
    botoes_frame = tk.Frame(remover)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Remover", command=lambda: backend.confirmar_remocao(produto, visor, remover), bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=1, column=0, padx=10, pady=20)
    tk.Button(botoes_frame, text="Cancelar", command=lambda: voltar_janela(remover, gerenciador), bg="#619999", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=1, column=1, padx=10, pady=20)


# Janela de editar produto
def janela_editar_produto(visor, gerenciador):
    editar = tk.Toplevel()
    editar.title("Editar Produto")
    editar.geometry("400x600")

    tk.Label(editar, text="Digite o ID do produto para editar:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    produto_id = tk.Entry(editar, width=30)
    produto_id.pack(pady=5)

    tk.Button(editar, text="Carregar Dados", command=lambda: backend.carregar_dados_produto(produto_id, nome_produto, categoria, quantidade, preco), bg="#619999", fg="#ffffff", font=("Helvetica", 12), width=15,).pack(pady=20)
    
    tk.Label(editar, text="Nome do Produto:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    nome_produto = tk.Entry(editar, width=30)
    nome_produto.pack(pady=5)

    tk.Label(editar, text="Categoria:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    categoria = tk.Entry(editar, width=30)
    categoria.pack(pady=5)

    tk.Label(editar, text="Quantidade:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    quantidade = tk.Entry(editar, width=30)
    quantidade.pack(pady=5)

    tk.Label(editar, text="Preço (R$):", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=5)
    preco = tk.Entry(editar, width=30)
    preco.pack(pady=5)

    botoes_frame = tk.Frame(editar)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Alterações", command=lambda: backend.salvar_edicao_produto(produto_id, nome_produto, categoria, quantidade, preco, visor, editar), bg="#005500", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=1, padx=10, pady=20)
    tk.Button(botoes_frame, text="Cancelar", command=lambda: voltar_janela(editar, gerenciador), bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=1, column=1, padx=10, pady=20)


# Janela de gerar relatório
def janela_gerar_relatorio(visor, gerenciador):
    relatorio = tk.Toplevel()
    relatorio.title("Relatório de Produtos")
    relatorio.geometry("700x400")

    tk.Label(relatorio, text="Relatório de Produtos", font=("Helvetica", 16)).pack(pady=10)

    visor = ttk.Treeview(relatorio, columns=("ID", "Nome", "Categoria", "Quantidade", "Preço"), show="headings")
    visor.heading("ID", text="ID")
    visor.heading("Nome", text="Nome")
    visor.heading("Categoria", text="Categoria")
    visor.heading("Quantidade", text="Quantidade")
    visor.heading("Preço", text="Preço (R$)")
    visor.column("ID", width=50)
    visor.column("Nome", width=200)
    visor.column("Categoria", width=200)
    visor.column("Quantidade", width=80)
    visor.column("Preço", width=80)
    visor.pack(pady=10)

    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    
    for produto in produtos:
        visor.insert("", "end", values=produto)
    conn.close()

    # Exportar a tabela com os produtos para um arquivo csv
    def exportar_csv():
        caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files", "*.csv")],title="Salvar Relatório")
    
        if caminho_arquivo:
            try:
                conn = sqlite3.connect('sistema.db')
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM produtos")
                produtos = cursor.fetchall()
                # Percorre a lista com os produtos puxado no BD, e lista cada um em cada linha no arquivo csv
                with open(caminho_arquivo, mode="w", newline="") as arquivo_csv:
                    writer = csv.writer(arquivo_csv)                    
                    writer.writerow(["ID", "Nome", "Categoria", "Quantidade", "Preço"])
                    for produto in produtos:
                        writer.writerow(produto)
                
                messagebox.showinfo("Exportação Completa", f"Produtos exportados com sucesso para {caminho_arquivo}")
            except sqlite3.Error as e:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao exportar produtos: {e}")
            finally:
                conn.close()
        else:
            messagebox.showinfo("Exportação Cancelada", "A exportação foi cancelada.")

    tk.Button(relatorio, text="Exportar CSV", command=exportar_csv, bg="#005500", fg="#ffffff", font=("Helvetica", 12), width=15).pack(pady=10)
    tk.Button(relatorio, text="Fechar", command=lambda: voltar_janela(relatorio, gerenciador), bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15).pack(pady=10)


# janela de gerenciamento
def janela_gerenciamento():
    gerenciador = tk.Toplevel()
    gerenciador.title("Sistema de Gerenciamento de Produtos")
    gerenciador.geometry("800x600")

    tk.Label(gerenciador, text="Bem-vindo ao sistema!", font=("Helvetica", 20), bg="#f0f0f0").pack(pady=10)

    tk.Label(gerenciador, text="Produtos Cadastrados:", font=("Helvetica", 14)).pack(pady=30)

    visor = ttk.Treeview(gerenciador, columns=("ID", "Nome", "Categoria", "Quantidade", "Preço"), show="headings")
    visor.heading("ID", text="ID")
    visor.heading("Nome", text="Nome")
    visor.heading("Categoria", text="Categoria")
    visor.heading("Quantidade", text="Quantidade")
    visor.heading("Preço", text="Preço")
    visor.column("ID", width=50)
    visor.column("Nome", width=200)
    visor.column("Categoria", width=200)
    visor.column("Quantidade", width=80)
    visor.column("Preço", width=80)
    visor.pack(pady=10)

    botoes_frame = tk.Frame(gerenciador)
    botoes_frame.pack(pady=10)

    def sair_sistema():
        gerenciador.destroy()
        janela_principal()

    tk.Button(botoes_frame, text="Cadastrar Produto", command=lambda: janela_cadastro_produto(visor, gerenciador), bg="#619999", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=1, padx=10, pady=20)
    tk.Button(botoes_frame, text="Editar Produto", command=lambda: janela_editar_produto(visor, gerenciador), bg="#619999", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=2, padx=10, pady=20)
    tk.Button(botoes_frame, text="Remover Produto", command=lambda: janela_remover_produto(visor, gerenciador), bg="#619999", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=3, padx=10, pady=20)
    tk.Button(botoes_frame, text="Gerar Relatório", command=lambda: janela_gerar_relatorio(visor, gerenciador), bg="#619999", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=0, column=4, padx=10, pady=20)
    tk.Button(botoes_frame, text="Sair do Sistema", command=sair_sistema, bg="#660000", fg="#ffffff", font=("Helvetica", 12), width=15,).grid(row=1, column=4, padx=10, pady=20)

    backend.atualizar_lista_produtos(visor)


if __name__ == "__main__":
    backend.criar_database()
    janela_principal()