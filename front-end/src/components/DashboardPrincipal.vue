<template>
  <div class="dashboard-container">
    
    <header class="cabecalho">
      <h1>Gerenciador de Documentos</h1>
      
      <div class="botoes">
        <!-- Botão para voltar ao Login -->
        <router-link to="/" class="botao-voltar">
          Sair
        </router-link>

        <router-link to="/upload" class="botao-novo">
          + Novo Upload
        </router-link>
      </div>
    </header>

    <div class="barra-pesquisa">
      <input type="text" placeholder="Pesquisar documentos..." />
    </div>
    
  </div>
</template>

<style scoped>
/* Visual Minimalista Preto e Branco */
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
  gap: 15px; /* Espaço entre os botões */
}

/* Estilo do botão novo (Principal) */
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

/* Estilo do botão voltar/sair (Secundário) */
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
  margin-bottom: 40px;
  box-sizing: border-box; 
}
</style>