<template>
  <div class="dashboard-container">
    
    <header class="cabecalho">
      <h1>Gerenciador de Documentos</h1>
      
      <router-link to="/upload" class="botao-novo">
        + Novo Upload
      </router-link>
    </header>

    <div class="barra-pesquisa">
      <input type="text" placeholder="Pesquisar documentos ou pastas..." />
    </div>

    <main class="area-pastas">
      <h2>Suas Pastas</h2>
      <div class="grade-pastas">
        <div class="pasta">📁 Contratos</div>
        <div class="pasta">📁 Recibos</div>
        <div class="pasta">📁 Pessoal</div>
      </div>
    </main>
    
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

.botao-novo {
  background-color: #000;
  color: #fff;
  padding: 10px 20px;
  text-decoration: none; /* Tira o sublinhado padrão do link */
  font-weight: bold;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.botao-novo:hover {
  background-color: #444;
}

.barra-pesquisa input {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  border: 2px solid #000;
  border-radius: 5px;
  margin-bottom: 40px;
  box-sizing: border-box; /* Garante que o padding não quebre a largura */
}

.area-pastas h2 {
  margin-bottom: 20px;
  font-size: 20px;
}

.grade-pastas {
  display: flex;
  gap: 20px;
}

.pasta {
  border: 2px solid #000;
  padding: 20px;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.pasta:hover {
  background-color: #000;
  color: #fff;
}
</style>