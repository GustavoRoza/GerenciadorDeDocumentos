<template>
  <div class="tela-inteira" :class="{ 'tema-escuro': modoEscuro }">
    
    <button @click="alternarTema" class="botao-tema">
      {{ modoEscuro ? '☀️ Modo Claro' : '🌙 Modo Escuro' }}
    </button>

    <div class="container">
      <h2 class="titulo">Teste de Upload</h2>
      
      <div class="area-upload">
        <input 
          type="file" 
          @change="lidarComSelecao" 
          accept="application/pdf" 
          class="input-arquivo"
        />
        
        <button @click="fazerUpload" class="botao-enviar">
          Enviar Arquivo
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const arquivo = ref(null);


const modoEscuro = ref(false);


const alternarTema = () => {
  modoEscuro.value = !modoEscuro.value;
};

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

<style scoped>

.tela-inteira {
  display: flex;
  justify-content: center; 
  align-items: center;     
  min-height: 100vh;       
  background-color: #f4f4f9; 
  transition: background-color 0.3s;
}

.container {
  width: 100%;
  max-width: 500px;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.titulo {
  color: #333;
  margin-bottom: 30px;
  transition: color 0.3s;
}

.area-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.input-arquivo {
  padding: 15px;
  border: 2px dashed #ccc;
  border-radius: 8px;
  width: 100%;
  max-width: 350px;
  cursor: pointer;
  background-color: #f9f9f9;
  color: #333;
  transition: all 0.3s;
}

.botao-enviar {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100%;
  max-width: 200px;
}

.botao-enviar:hover {
  background-color: #45a049;
}

.botao-tema {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: transparent;
  border: 2px solid #ccc;
  padding: 8px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  color: #555;
  transition: all 0.3s;
}

.botao-tema:hover {
  background-color: #e0e0e0;
}


.tema-escuro {
  background-color: #121212;
}

.tema-escuro .container {
  background-color: #1e1e1e;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.tema-escuro .titulo {
  color: #e0e0e0;
}

.tema-escuro .input-arquivo {
  background-color: #2d2d2d;
  border-color: #555;
  color: #e0e0e0;
}

.tema-escuro .botao-tema {
  border-color: #555;
  color: #e0e0e0;
}

.tema-escuro .botao-tema:hover {
  background-color: #333;
}
</style>