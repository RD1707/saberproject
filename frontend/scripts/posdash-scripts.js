function expandirRelatorio(index) {
    const detalhes = document.getElementById(`relatorio-detalhes-${index}`);
    if (!detalhes) {
        console.error(`Detalhes do relatório ${index} não encontrados.`);
        return;
    }

    detalhes.classList.toggle('ativo'); // Alterna a classe para expandir/recolher
}

function carregarAtividadesRecentes() {
    const listaAtividades = document.getElementById('atividades-recentes');
    if (!listaAtividades) {
        console.error('Elemento "atividades-recentes" não encontrado no DOM.');
        return;
    }

    fetch('http://localhost:5000/consultar-atividades-recentes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario_id: localStorage.getItem('usuario_id') })
    })
    .then(response => response.json())
    .then(data => {
        listaAtividades.innerHTML = '';

        if (data.status === 'success' && data.atividades.length > 0) {
            data.atividades.forEach(atividade => {
                const item = document.createElement('li');
                item.classList.add('atividade-item');
                item.innerHTML = `
                    <h3>${atividade.nome_aluno || 'N/A'}</h3>
                    <p><strong>Matéria:</strong> ${atividade.materia || 'N/A'}</p>
                    <p><strong>Atividade:</strong> ${atividade.atividade || 'N/A'}</p>
                    <p><strong>Data:</strong> ${atividade.data_criacao || 'N/A'}</p>
                `;
                listaAtividades.appendChild(item);
            });
        } else {
            listaAtividades.innerHTML = '<li>Nenhuma atividade recente encontrada.</li>';
        }
    })
    .catch(error => {
        console.error('Erro ao carregar atividades recentes:', error);
    });
}

function carregarRelatorios() {
    const listaRelatorios = document.getElementById('lista-relatorios');
    const relatoriosCount = document.getElementById('relatorios-gerados-count');
    const filtroMateria = document.getElementById('filtro-materia').value;
    const filtroAluno = document.getElementById('filtro-aluno').value;
    const filtroData = document.getElementById('filtro-data').value;

    if (!listaRelatorios || !relatoriosCount) {
        console.error('Elementos dos relatórios não encontrados no DOM.');
        return;
    }

    fetch('http://localhost:5000/consultar-relatorios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario_id: localStorage.getItem('usuario_id'), materia: filtroMateria, aluno: filtroAluno, data: filtroData })
    })
    .then(response => response.json())
    .then(data => {
        listaRelatorios.innerHTML = '';

        if (data.status === 'success' && data.relatorios.length > 0) {
            relatoriosCount.textContent = `${data.relatorios.length} relatórios gerados`;

            data.relatorios.forEach((relatorio, index) => {
                const item = document.createElement('div');
                item.classList.add('relatorio-item');

                item.innerHTML = `
                    <div class="relatorio-cabecalho" onclick="expandirRelatorio(${index})">
                        <h3>${relatorio.nome_aluno} - ${relatorio.materia}</h3>
                        <p><strong>Atividade:</strong> ${relatorio.atividade}</p>
                    </div>
                    <div class="relatorio-detalhes" id="relatorio-detalhes-${index}">
                        <p><strong>Pergunta:</strong> ${relatorio.pergunta}</p>
                        <p><strong>Resposta:</strong> ${relatorio.resposta}</p>
                        <p><strong>Relatório:</strong> ${relatorio.relatorio}</p>
                    </div>
                `;

                listaRelatorios.appendChild(item);
            });
        } else {
            relatoriosCount.textContent = '0 relatórios gerados';
            listaRelatorios.innerHTML = '<p>Nenhum relatório encontrado.</p>';
        }
    })
    .catch(error => {
        console.error('Erro ao carregar relatórios:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const usuario_id = localStorage.getItem('usuario_id');

    if (!usuario_id) {
        alert('Usuário não logado.');
        window.location.href = 'index.html';
        return;
    }

    document.getElementById('btn-relatorios').addEventListener('click', function () {
        document.querySelector('.recent-activities').style.display = 'none';
        document.getElementById('relatorios').style.display = 'block';
        document.getElementById('configuracoes').style.display = 'none';
        carregarRelatorios();
    });

    document.getElementById('btn-configuracoes').addEventListener('click', function () {
        document.getElementById('relatorios').style.display = 'none';
        document.getElementById('configuracoes').style.display = 'block';
        document.querySelector('.recent-activities').style.display = 'none';
    });

    const btnAplicarFiltros = document.getElementById('aplicar-filtros');
    if (btnAplicarFiltros) {
        btnAplicarFiltros.addEventListener('click', function(event) {
            event.preventDefault();
            carregarRelatorios();
        });
    }

    document.getElementById('sair-conta').addEventListener('click', function() {
        localStorage.removeItem('usuario_id');
        window.location.href = 'index.html';
    });

    document.getElementById('voltar-escolha').addEventListener('click', function(event) {
        event.preventDefault();
        window.location.href = 'escolha.html';
    });

    carregarAtividadesRecentes();
});

document.addEventListener('DOMContentLoaded', function() {
    const savedEvents = JSON.parse(localStorage.getItem('saberEvents') || '[]');
    
    const miniCalendarEl = document.getElementById('calendar');
    const miniCalendar = new FullCalendar.Calendar(miniCalendarEl, {
        initialView: 'dayGridMonth', 
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: ''
        },
        events: savedEvents, 
        eventClick: function(info) {
            alert(`Evento: ${info.event.title}\nDescrição: ${info.event.extendedProps.description}`);
        }
    });

    miniCalendar.render();
});
