from flask import Flask, jsonify, request, send_from_directory
import cohere
from flask_cors import CORS
from database.bdsaber import buscar_usuarios, inserir_cadastro, DB_PATH, conectar
import os

# Inicializa o Flask
app = Flask(__name__)
CORS(app)

# Iniciar o cliente Cohere
cohere_api_key = "6LZJ0P3YguU31e91MZLBfkCcK4NdlELvZcisx7Jg"
co = cohere.Client(cohere_api_key)

# Rota para autenticação de login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('username')
    senha = data.get('password')

    usuario = buscar_usuarios(login, senha)
    if usuario:
        return jsonify({'status': 'success', 'message': 'Login realizado com sucesso!'})
    else:
        return jsonify({'status': 'error', 'message': 'Usuário ou senha incorretos.'}), 401

# Rota para registro de usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nome_completo = data.get('nome_completo')
    email = data.get('email')
    cpf = data.get('cpf')
    senha = data.get('senha')

    try:
        inserir_cadastro(nome_completo, email, cpf, senha)
        return jsonify({'status': 'success', 'message': 'Registro realizado com sucesso!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Função para gerar relatório
def gerar_relatorio_educacional(questao, resposta_aluno, materia):
    prompt = f"""
    Você é uma IA educacional do sistema SABER. Sua tarefa é avaliar o desempenho dos alunos, dialogar com o professor e sugerir dicas de atividades.
    Aqui está uma pergunta de um exame: "{questao}". 
    A resposta do aluno foi: "{resposta_aluno}". 
    O tema desta questão é: "{materia}". 
    Avalie a resposta do aluno, ofereça um feedback objetivo e sugira rapidamente uma atividade ou recurso de estudo para o professor usar para ajudar o aluno. Você é uma IA educacional. Avalie a resposta do aluno com base na clareza, correção e completude.  
Dê uma nota de 0 a 10 e explique brevemente sua avaliação, organize bem o texto, deixe a nota em uma linha, o feedback em outra e a atividade sugerida em outra.

    """
    try:
        response = co.generate(
            model='command-r-08-2024',
            prompt=prompt,
            max_tokens=250  
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return "Erro ao gerar relatório."

# Função para salvar relatório no banco de dados
def salvar_relatorio(usuario_id, nome_aluno, turma, materia, atividade, pergunta, resposta, relatorio):
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute('''
        INSERT INTO relatorios (usuario_id, nome_aluno, turma, materia, atividade, pergunta, resposta, relatorio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome_aluno, turma, materia, atividade, pergunta, resposta, relatorio))
        con.commit()
        con.close()
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")

# Rota para gerar e salvar relatório
@app.route('/gerar-relatorio', methods=['POST'])
def gerar_relatorio():
    dados = request.json
    usuario_id = dados.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'status': 'error', 'message': 'Usuário não autenticado.'}), 401

    # Gera o relatório
    relatorio = gerar_relatorio_educacional(
        dados['pergunta'], 
        dados['resposta'], 
        dados['materia']
    )

    # Salva no banco de dados
    salvar_relatorio(
        usuario_id=usuario_id,
        nome_aluno=dados['nome_aluno'],
        turma=dados['turma'],
        materia=dados['materia'],
        atividade=dados['atividade'],
        pergunta=dados['pergunta'],
        resposta=dados['resposta'],
        relatorio=relatorio
    )

    return jsonify({'relatorio': relatorio, 'status': 'success'}), 200

# Rota para servir o dashboard
@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard-index.html')

# Rota para servir a página de login
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Rota para consultar relatórios gerados por um usuário
@app.route('/consultar-relatorios', methods=['POST'])
def consultar_relatorios():
    data = request.json
    usuario_id = data.get('usuario_id')

    if not usuario_id:
        return jsonify({'status': 'error', 'message': 'ID do usuário não fornecido.'}), 400

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute('''
            SELECT nome_aluno, turma, materia, atividade, pergunta, resposta, relatorio, data_criacao 
            FROM relatorios 
            WHERE usuario_id = ?
        ''', (usuario_id,))
        
        relatorios = []
        for row in cur.fetchall():
            relatorios.append({
                "nome_aluno": row[0],
                "turma": row[1],
                "materia": row[2],
                "atividade": row[3],
                "pergunta": row[4],
                "resposta": row[5],
                "relatorio": row[6],
                "data_criacao": row[7]
            })
        
        con.close()
        print(f"Relatórios encontrados: {relatorios}")  # Log para depuração
        return jsonify({'status': 'success', 'relatorios': relatorios}), 200
    except Exception as e:
        print(f"Erro ao consultar relatórios: {e}")  # Log para depuração
        return jsonify({'status': 'error', 'message': 'Erro ao consultar relatórios.'}), 500

@app.route('/consultar-atividades-recentes', methods=['POST'])
def consultar_atividades_recentes():
    data = request.json
    usuario_id = data.get('usuario_id')

    if not usuario_id:
        return jsonify({'status': 'error', 'message': 'ID do usuário não fornecido.'}), 400

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute('''
            SELECT nome_aluno, materia, atividade, data_criacao 
            FROM relatorios 
            WHERE usuario_id = ?
            ORDER BY data_criacao DESC
            LIMIT 5
        ''', (usuario_id,))
        
        atividades = []
        for row in cur.fetchall():
            atividades.append({
                "nome_aluno": row[0],
                "materia": row[1],
                "atividade": row[2],
                "data_criacao": row[3]
            })
        
        con.close()
        return jsonify({'status': 'success', 'atividades': atividades}), 200
    except Exception as e:
        print(f"Erro ao consultar atividades recentes: {e}")
        return jsonify({'status': 'error', 'message': 'Erro ao consultar atividades recentes.'}), 500

if __name__ == '__main__':
    app.run(debug=True)