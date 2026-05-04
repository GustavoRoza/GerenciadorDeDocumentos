<template>
  <div class="tela-inteira">
    <div class="container">
      
      <!-- Novo topo com botão de voltar -->
      <div class="topo-container">
        <router-link to="/dashboard" class="botao-voltar">
          ← Voltar
        </router-link>
      </div>

      <h2 class="titulo">Teste de Upload</h2>
      
      <div class="area-upload">
        <input 
          type="file" 
          @change="lidarComSelecao" 
          accept="application/pdf" 
          class="input-arquivo"
          :disabled="carregando"
        />
        
        <button 
          @click="fazerUpload" 
          class="botao-enviar" 
          :disabled="carregando"
        >
          {{ carregando ? 'Enviando...' : 'Enviar Arquivo' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const arquivo = ref(null);
const carregando = ref(false);

const lidarComSelecao = (evento) => {
  arquivo.value = evento.target.files[0];
};

const fazerUpload = async () => {
  if (!arquivo.value) {
    alert("Por favor, selecione um arquivo primeiro.");
    return;
  }

  carregando.value = true; 
  
  const formData = new FormData();
  formData.append("file", arquivo.value);

  try {
    const resposta = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (resposta.ok) {
      alert("Upload realizado com sucesso!");
      arquivo.value = null; 
    } else {
      alert("Erro no upload. Verifique o backend.");
    }
  } catch (erro) {
    console.error("Erro na comunicação com a API:", erro);
    alert("Erro ao conectar com o servidor. O FastAPI está rodando?");
  } finally {
    carregando.value = false; 
  }
};
</script>

<style scoped>
.tela-inteira {
  display: flex;
  justify-content: center; 
  align-items: center;     
  min-height: 100vh;       
  background-color: #f4f4f9; 
}

.container {
  width: 100%;
  max-width: 500px;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative; /* Adicionado para organizar o topo */
}

/* Layout do topo para alinhar o botão à esquerda */
.topo-container {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 10px;
}

/* Estilo do botão voltar (Secundário) */
.botao-voltar {
  background-color: transparent;
  color: #000;
  padding: 8px 15px;
  text-decoration: none;
  font-weight: bold;
  font-size: 14px;
  border: 2px solid #000;
  border-radius: 5px;
  transition: all 0.3s;
}

.botao-voltar:hover {
  background-color: #000;
  color: #fff;
}

.titulo {
  color: #000;
  margin-bottom: 30px;
}

.area-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.input-arquivo {
  padding: 15px;
  border: 2px dashed #000;
  border-radius: 8px;
  width: 100%;
  max-width: 350px;
  cursor: pointer;
  background-color: #f9f9f9;
  color: #000;
  transition: opacity 0.3s;
}

.input-arquivo:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.botao-enviar {
  background-color: #000;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s;
  width: 100%;
  max-width: 200px;
}

.botao-enviar:hover:not(:disabled) {
  background-color: #333;
}

.botao-enviar:disabled {
  background-color: #666;
  opacity: 0.7;
  cursor: not-allowed;
}
</style>