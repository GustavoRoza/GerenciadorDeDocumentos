<template>
  <div style="padding: 40px; font-family: sans-serif;">
    <h2>Teste de Upload do DocBrain</h2>
    
    <input 
      type="file" 
      @change="lidarComSelecao" 
      accept="application/pdf" 
    />
    
    <button 
      @click="fazerUpload" 
      style="margin-left: 10px; padding: 5px 15px;"
    >
      Enviar Arquivo
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const arquivo = ref(null);

const lidarComSelecao = (evento) => {
  arquivo.value = evento.target.files[0];
};

const fazerUpload = async () => {
  if (!arquivo.value) {
    alert("Por favor, selecione um arquivo primeiro.");
    return;
  }

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
  }
};
</script>