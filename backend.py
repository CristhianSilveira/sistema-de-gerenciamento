import sqlite3
import main as main
from tkinter import messagebox


# Criar as tabelas no BD através do database.sql
def criar_database():
    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        # Ler o arquivo SQL
        with open('database.sql', 'r') as f:
            sql = f.read()
        
        cursor.executescript(sql)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao se conectar ao Banco de Dados: {e}")
    finally: 
        conn.close()


# Cadastrar o usuário no BD
def cadastrar_usuario(nome, sobrenome, email, senha, janela_cadastro):
    # Verifica se a entrada de login e senha estão vazios
    if not email or not senha:
        messagebox.showerror("Erro", "Os campos de email e senha não podem estar vazios.")
        return

    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, sobrenome, email, senha)
            VALUES (?, ?, ?, ?)
        ''', (nome, sobrenome, email, senha))
        conn.commit()
        
        messagebox.showinfo("Cadastro", f"Usuário {nome} cadastrado com sucesso!")
        
        janela_cadastro.destroy()
        main.janela_principal()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Usuário já cadastrado!")
    finally:
        conn.close()


# Validação básica de usuario e senha
def validacao_login(janela_login, email, senha):
    email = email.get()
    senha = senha.get() 

    if not email or not senha:
            messagebox.showerror("Erro", "Os campos de email e senha não podem estar vazios.")
            return 
    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        user = cursor.fetchone() #Retorna uma tupla com apenas um resultado

        if user:
            janela_login.destroy()
            main.janela_gerenciamento()
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos!")
    except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao procurar usuário: {e}")
    finally:
        conn.close()      


# Atualiza a lista/tabela de produtos
def atualizar_lista_produtos(visor):
    # Percorre cada linha do visor e remove o item
    for item in visor.get_children():
        visor.delete(item)

    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall() # Cria uma tupla com todos os resultado do comando sql

        # Percorre cada produto do BD e coloca no visor
        for produto in produtos:
            visor.insert("", "end", values=produto)
    except sqlite3.Error as e:
        messagebox.showerror(f"Erro ao carregar produtos: {e}")
    finally:
        conn.close()


def salvar_produto(nome_produto, categoria, quantidade, preco, cadastro_produto, visor):
        nome_produto_valor = nome_produto.get()
        categoria_valor = categoria.get()
        quantidade_valor = quantidade.get()
        preco_valor = preco.get()

        if not nome_produto_valor or not categoria_valor:
            messagebox.showerror("Erro", "Os campos de Produto e Categoria não podem estar vazios.")
            return
        try:
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO produtos (nome, categoria, quantidade, preco)
                VALUES (?, ?, ?, ?)
            ''', (nome_produto_valor, categoria_valor, int(quantidade_valor), float(preco_valor)))

            conn.commit()     
            messagebox.showinfo("Cadastro de Produto", f"Produto '{nome_produto_valor}' cadastrado com sucesso!")
            
            cadastro_produto.destroy()
            atualizar_lista_produtos(visor)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e preço devem ser números!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao cadastrar produto: {e}")
        finally:
            conn.close()


def confirmar_remocao(produto, visor, janela_remover):
        produto_id = produto.get()

        if not produto_id.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um ID válido.")
            return

        try:
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
            produto_id_existe = cursor.fetchone()

            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            
            if produto_id_existe:
                messagebox.showinfo("Sucesso", f"Produto com ID {produto_id} removido com sucesso.")
                janela_remover.destroy()
            else:
                messagebox.showerror("Erro", "Produto não encontrado!")
            
            atualizar_lista_produtos(visor)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao tentar remover o produto: {e}")
        finally:
            conn.close()


# Verifica se o produto existe no BD
def carregar_dados_produto(produto_id, nome_produto, categoria, quantidade, preco):
    produto_edit = produto_id.get()
    verifica_vazio = [nome_produto.get(), categoria.get(), quantidade.get(), preco.get()]

    if not produto_edit.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")
        return
    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()            
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_edit,))
        produto = cursor.fetchone()

        # Verifica se a lista com as entradas estão sem texto, se estiver com texto ele limpa ao apertar no botão "carregar dados"
        if all(campo == "" for campo in verifica_vazio):
            if produto:
                nome_produto.insert(0, produto[1])
                categoria.insert(0, produto[2])
                quantidade.insert(0, produto[3])
                preco.insert(0, produto[4])
            else:
                messagebox.showerror("Erro", "Produto não encontrado!")
        else:
            nome_produto.delete(0, 'end')
            categoria.delete(0, 'end')
            quantidade.delete(0, 'end')
            preco.delete(0, 'end')
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao tentar editar o Produto {e}")
    finally:
        conn.close()


# Atualiza as alterações no BD
def salvar_edicao_produto(produto_id, nome_produto, categoria, quantidade, preco, visor, editar):
    produto_novo = produto_id.get()
    nome_novo = nome_produto.get()
    categoria_nova = categoria.get()
    quantidade_nova = quantidade.get()
    preco_novo = preco.get()

    if not nome_novo or not categoria_nova:
        messagebox.showerror("Erro", "Os campos de Produto e Categoria não podem estar vazios.")
        return 
    
    try:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos
            SET nome = ?, categoria = ?, quantidade = ?, preco = ?
            WHERE id = ?
        ''', (nome_novo, categoria_nova, int(quantidade_nova), float(preco_novo), produto_novo))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        atualizar_lista_produtos(visor)
        editar.destroy()
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preço devem ser números!")
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao editar produto: {e}")
    finally:
        conn.close()