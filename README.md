# SABER (Sistema de Análise e Benefício Educacional em Relatório)

## Descrição
O SABER é uma plataforma educacional que utiliza inteligência artificial para analisar o desempenho dos alunos e gerar relatórios personalizados. O objetivo é auxiliar professores na identificação de dificuldades específicas, permitindo a aplicação de intervenções mais direcionadas e eficazes. 

A IA da plataforma interage com as respostas dos alunos, oferecendo feedback em tempo real e ajustando relatórios com base no desempenho, utilizando técnicas avançadas de análise de linguagem natural.

## Funcionalidades
- Análise automática de respostas de alunos
- Geração de relatórios personalizados com base no desempenho
- Detecção de similaridade de respostas e compreensão usando a API Cohere
- Interatividade para solicitar novas atividades ou finalizar o uso
- Relatorio Geral da turma
- Correção de Redação
- Estatisticas do aluno e da turma em graficos e tabelas
- Cadastro de provas, atividades e etc no painel do professor

## Tecnologias Utilizadas
- **Python** para o desenvolvimento do sistema
- **Cohere API** para detecção de similaridade e compreensão de texto
- **Terminal** para a interação inicial
- **Tkinter** para a interface

## Pré-requisitos
Antes de instalar o SABER, certifique-se de que você tem:
- Python 3.7 ou superior
- Um ambiente virtual configurado (opcional, mas recomendado)
- Acesso à API da OpenAI e Cohere

## Instalação
1. Clone este repositório:
    ```bash
    git clone (https://github.com/WerKdev/SABER)
    cd SABER
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/macOS
    venv\Scripts\activate # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install cohere
    pip install sqlite3
    pip install customtkinter
    ```

## Uso
Para executar o protótipo do SABER no terminal, siga os passos abaixo:

1. Execute o script principal:
    ```bash
    python main.py
    ```

2. A IA solicitará as respostas dos alunos e gerará relatórios com base nas interações.

Contribuições são bem-vindas! Se você deseja contribuir com o desenvolvimento do SABER, siga os seguintes passos:

1. Faça um fork do projeto
2. Crie uma nova branch para suas modificações:
    ```bash
    git checkout -b feature/nova-funcionalidade
    ```
3. Faça o commit das suas alterações:
    ```bash
    git commit -m 'Adiciona nova funcionalidade'
    ```
4. Envie as alterações para o seu fork:
    ```bash
    git push origin feature/nova-funcionalidade
    ```
5. Abra um pull request no repositório principal.

Desenvolvido com Python por RD1707 e WerKdev.
