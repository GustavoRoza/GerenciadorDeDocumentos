<template>
  <div class="dashboard-container">
    
    <header class="cabecalho">
      <h1>Gerenciador de Documentos</h1>
      
      <div class="botoes">
        <router-link to="/" class="botao-voltar">
          Sair
        </router-link>

        <router-link to="/upload" class="botao-novo">
          + Novo Upload
        </router-link>
      </div>
    </header>
    
    <div class="estatisticas-container" v-if="estatisticas.length > 0">
      <div v-for="stat in estatisticas" :key="stat.tipo" class="card-estatistica">
        <span class="tipo-arquivo">{{ formatarTipo(stat.tipo) }}</span>
        <span class="quantidade-arquivo">{{ stat.quantidade }} salvos</span>
      </div>
    </div>
    
    <div class="barra-pesquisa">
      <input 
        type="text" 
        v-model="termoPesquisa"
        @input="executarBusca"
        placeholder="Pesquisar por conteúdo, palavras-chave ou resumo..." 
      />
    </div>

    <div class="lista-documentos">
      <div v-if="carregando" class="mensagem-estado">Buscando documentos...</div>
      
      <div v-else-if="documentos.length === 0 && termoPesquisa.trim() !== ''" class="mensagem-estado">
        Nenhum documento encontrado para esta pesquisa.
      </div>

      <div v-else v-for="doc in documentos" :key="doc.id" class="card-documento">
        <div class="topo-card">
          <span class="nome-arquivo">📄 {{ doc.nome_original }}</span>
          <span class="data-arquivo">{{ formatarData(doc.data_criacao) }}</span>
        </div>
        <div class="conteudo-card">
          <p class="titulo-resumo">Resumo da IA:</p>
          <p class="texto-resumo">{{ doc.resumo_ia || 'Este documento não possui resumo disponível.' }}</p>
        </div>
        
        <div class="acoes-card" v-if="doc.url_download">
          <a :href="doc.url_download" target="_blank" rel="noopener noreferrer" class="botao-baixar">
            ⬇ Baixar Arquivo
          </a>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const termoPesquisa = ref('');
const documentos = ref([]);
const estatisticas = ref([]);
const carregando = ref(false);

let timeoutBusca = null;
let timeoutLimpeza = null; // Novo controle para limpar a tela após um tempo

// Tempo que os resultados ficam na tela (em milissegundos). Ex: 60000 = 60 segundos
const TEMPO_LIMPEZA_AUTOMATICA = 60000; 

// Função que faz a requisição para o endpoint do FastAPI
const executarBusca = () => {
  clearTimeout(timeoutBusca);
  clearTimeout(timeoutLimpeza); // Cancela a limpeza anterior se o usuário voltar a digitar

  const termo = termoPesquisa.value.trim();

  // Se o campo estiver vazio, limpa a tela e não faz a requisição
  if (!termo) {
    documentos.value = [];
    return;
  }

  // debounce simples para não sobrecarregar o servidor
  timeoutBusca = setTimeout(async () => {
    carregando.value = true;
    try {
      const url = `http://localhost:8000/documentos/buscar?q=${encodeURIComponent(termo)}`;
      const resposta = await fetch(url);
      
      if (resposta.ok) {
        documentos.value = await resposta.json();

        // INICIA O CRONÔMETRO PARA LIMPAR A TELA SOZINHA
        timeoutLimpeza = setTimeout(() => {
          documentos.value = [];
          termoPesquisa.value = ''; // Limpa também o que foi digitado
        }, TEMPO_LIMPEZA_AUTOMATICA);

      } else {
        console.error("Erro na resposta do servidor");
      }
    } catch (erro) {
      console.error("Erro ao buscar documentos:", erro);
    } finally {
      carregando.value = false;
    }
  }, 300);
};

// Formata a data retornada pelo banco para o padrão brasileiro
const formatarData = (dataString) => {
  if (!dataString) return '';
  const data = new Date(dataString);
  return data.toLocaleDateString('pt-BR') + ' ' + data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
};

const buscarEstatisticas = async () => {
  try {
    const url = `http://localhost:8000/documentos/estatisticas`;
    const resposta = await fetch(url);
    if (resposta.ok) {
      estatisticas.value = await resposta.json();
    }
  } catch (erro) {
    console.error("Erro ao buscar estatísticas:", erro);
  }
};

const formatarTipo = (mimetype) => {
  if (mimetype === 'application/pdf') return 'PDF';
  
  if (mimetype && mimetype.includes('/')) {
    return mimetype.split('/')[1].toUpperCase();
  }
  return mimetype;
};

onMounted(() => {
  // REMOVIDO: executarBusca(); 
  // Agora só busca as estatísticas ao abrir a tela. A busca de arquivos só ocorre ao digitar.
  buscarEstatisticas();
});
</script>

<style scoped>
/* Mantendo o padrão Minimalista Preto e Branco (sem alterações no seu CSS original) */
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: Arial, sans-serif;
  color: #000; 
}

.cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #000;
  padding-bottom: 20px;
  margin-bottom: 30px;
}

h1 {
  margin: 0;
  font-size: 28px;
}

.botoes {
  display: flex;
  gap: 15px;
}

.botao-novo {
  background-color: #000;
  color: #fff;
  padding: 10px 20px;
  text-decoration: none; 
  font-weight: bold;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.botao-novo:hover {
  background-color: #444;
}

.botao-voltar {
  background-color: transparent;
  color: #000;
  padding: 10px 20px;
  text-decoration: none;
  font-weight: bold;
  border: 2px solid #000;
  border-radius: 5px;
  transition: all 0.3s;
}

.botao-voltar:hover {
  background-color: #000;
  color: #fff;
}

.barra-pesquisa input {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  border: 2px solid #000;
  border-radius: 5px;
  margin-bottom: 30px;
  box-sizing: border-box; 
  outline: none;
}

.barra-pesquisa input:focus {
  background-color: #f9f9f9;
}

.lista-documentos {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mensagem-estado {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 20px;
}

.card-documento {
  border: 2px solid #000;
  border-radius: 6px;
  padding: 20px;
  background-color: #fff;
}

.topo-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 12px;
}

.nome-arquivo {
  font-weight: bold;
  font-size: 16px;
}

.data-arquivo {
  font-size: 12px;
  color: #666;
}

.titulo-resumo {
  margin: 0 0 5px 0;
  font-size: 13px;
  font-weight: bold;
  color: #333;
}

.texto-resumo {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: #222;
  text-align: justify;
}

.estatisticas-container {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.card-estatistica {
  border: 2px solid #000;
  border-radius: 6px;
  padding: 15px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 150px;
}

.tipo-arquivo {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 5px;
  color: #333;
}

.quantidade-arquivo {
  font-size: 20px;
  font-weight: bold;
}

.acoes-card {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px dashed #ddd; 
  display: flex;
  justify-content: flex-end; 
}

.botao-baixar {
  background-color: transparent;
  color: #000;
  padding: 8px 16px;
  text-decoration: none;
  font-weight: bold;
  border: 2px solid #000;
  border-radius: 5px;
  transition: all 0.3s;
  font-size: 14px;
}

.botao-baixar:hover {
  background-color: #000;
  color: #fff;
}
</style>