document.getElementById('form-relatorio').addEventListener('submit', function(event) {
    event.preventDefault();

    console.log("Formulário enviado.");

    const nomeAluno = document.getElementById('nome-aluno').value;
    const turma = document.getElementById('turma').value;
    const materia = document.getElementById('materia').value;
    const atividade = document.getElementById('atividade').value;
    const pergunta = document.getElementById('pergunta').value;
    const resposta = document.getElementById('resposta').value;

    const usuario_id = localStorage.getItem('usuario_id');
    if (!usuario_id) {
        alert('Usuário não logado.');
        return;
    }

    console.log("Dados do formulário:", { nomeAluno, turma, materia, atividade, pergunta, resposta, usuario_id });

    const data = {
        nome_aluno: nomeAluno,
        turma: turma,
        materia: materia,
        atividade: atividade,
        pergunta: pergunta,
        resposta: resposta,
        usuario_id: usuario_id
    };

    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }

    fetch('http://localhost:5000/gerar-relatorio', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log("Resposta do servidor recebida:", response);
        return response.json();
    })
    .then(responseData => {
        console.log("Dados recebidos do servidor:", responseData);
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        
        // Se o servidor retornou erro
        if (!responseData || responseData.status === 'error') {
            console.error("Erro do servidor:", responseData.message || "Resposta inesperada.");
            alert("Erro ao gerar relatório. Verifique os dados e tente novamente.");
            return;
        }
    
        // Verifica se o campo 'relatorio' existe na resposta
        if (!responseData.relatorio) {
            console.error("Campo 'relatorio' não encontrado na resposta do servidor.");
            alert("Erro: relatório não gerado. Verifique o servidor.");
            return;
        }
        
        // Armazena o relatório gerado no localStorage com a chave "relatorioSalvo"
        localStorage.setItem('relatorioSalvo', JSON.stringify({
            nome_aluno: nomeAluno,
            turma: turma,
            materia: materia,
            atividade: atividade,
            pergunta: pergunta,
            resposta: resposta,
            relatorio: responseData.relatorio
        }));
        
        console.log("Redirecionando para relatorio-salvo.html");
        // Redireciona para a página de exibição do relatório
        window.location.href = 'relatorio-salvo.html'; // Certifique-se de que o caminho está correto
    })
    .catch(error => {
        console.error('Erro no fetch:', error);
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        alert('Erro ao gerar relatório. Verifique sua conexão e tente novamente.');
    });
});

// Adiciona o event listener para o botão "sair-conta", se existir
const btnSairConta = document.getElementById('sair-conta');
if (btnSairConta) {
    btnSairConta.addEventListener('click', function() {
        localStorage.removeItem('usuario_id');
        window.location.href = 'index.html';
    });
}

// Adiciona o event listener para o botão "voltar-escolha", se existir
const btnVoltarEscolha = document.getElementById('voltar-escolha');
if (btnVoltarEscolha) {
    btnVoltarEscolha.addEventListener('click', function(event) {
        event.preventDefault();
        window.location.href = 'escolha.html';
    });
}