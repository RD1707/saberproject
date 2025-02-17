import sqlite3
import tkinter.messagebox as tkmb
import os

# Obtém o caminho correto do banco dentro da pasta `database/`
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banco_saber.db")

# 🔹 Função para conectar ao banco de dados (corrige o erro!)
def conectar():
    return sqlite3.connect(DB_PATH)

# 🔹 Criar tabelas no banco de dados
def criar_tabela():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        CPF TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS relatorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        nome_aluno TEXT NOT NULL,
        turma TEXT NOT NULL,
        materia TEXT NOT NULL,
        atividade TEXT NOT NULL,
        pergunta TEXT NOT NULL,
        resposta TEXT NOT NULL,
        relatorio TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')
    con.commit()
    con.close()

# 🔹 Inserir novo usuário no banco
def inserir_cadastro(nome_completo, email, cpfn, senha):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute('''
        INSERT INTO usuarios (nome_completo, email, CPF, senha)
        VALUES (?, ?, ?, ?)
        ''', (nome_completo, email, cpfn, senha))
        con.commit()
        print("Cadastro inserido com sucesso.")
    except sqlite3.IntegrityError as e:
        if "email" in str(e).lower():
            tkmb.showerror("Erro no Cadastro", "Este e-mail já está cadastrado.")
        elif "cpf" in str(e).lower():
            tkmb.showerror("Erro no Cadastro", "Este CPF já está cadastrado.")
        else:
            tkmb.showerror("Erro no Cadastro", f"Erro ao inserir o cadastro: {e}")
    finally:
        con.close()

# 🔹 Buscar usuário no banco de dados (login)
def buscar_usuarios(login, senha):
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT * FROM usuarios WHERE (email = ? OR cpf = ?) AND senha = ?', (login, login, senha))
    usuario = cur.fetchone()
    con.close()
    return usuario  # Retorna `None` se o usuário não for encontrado

# 🔹 Consultar todos os usuários
def checar_bd():
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    con.close()
    return usuarios

# 🔹 Verificar se o email ou CPF já existe
def checkemailcpf(email, cpfn):
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT 1 FROM usuarios WHERE email = ? OR CPF = ?', (email, cpfn))
    resultado = cur.fetchone()
    con.close()
    return resultado is not None

# 🔹 Criar as tabelas na primeira execução
criar_tabela()
