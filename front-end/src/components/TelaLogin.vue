<template>
  <div class="tela-inteira">
    <div class="container-login">
      <h1 class="titulo-logo">Gerenciador de Documentos</h1>
      <p class="subtitulo">Faça login para acessar seus documentos</p>
      
      <form @submit.prevent="fazerLogin" class="formulario-login">
        <div class="grupo-input">
          <label for="usuario">Usuário</label>
          <input 
            type="text" 
            id="usuario"
            v-model="usuario"
            placeholder="Digite seu usuário" 
            required 
          />
        </div>

        <div class="grupo-input">
          <label for="senha">Senha</label>
          <input 
            type="password" 
            id="senha"
            v-model="senha"
            placeholder="Digite sua senha" 
            required 
          />
        </div>
        
        <button type="submit" class="botao-entrar">
          Entrar
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; 

const roteador = useRouter();

// A variável agora se chama 'usuario' em vez de 'email'
const usuario = ref('');
const senha = ref('');

const fazerLogin = () => {
  // A verificação agora checa se 'usuario' e 'senha' foram preenchidos
  if (usuario.value && senha.value) {
    roteador.push('/dashboard'); 
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

.container-login {
  width: 100%;
  max-width: 400px;
  padding: 50px 40px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: Arial, sans-serif;
}

.titulo-logo {
  color: #000;
  margin: 0 0 10px 0;
  font-size: 32px;
}

.subtitulo {
  color: #666;
  margin-bottom: 30px;
  font-size: 14px;
}

.formulario-login {
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: left;
}

.grupo-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.grupo-input label {
  font-size: 14px;
  font-weight: bold;
  color: #000;
}

.grupo-input input {
  padding: 12px;
  border: 2px solid #000;
  border-radius: 8px;
  font-size: 16px;
  background-color: #f9f9f9;
  color: #000;
  outline: none;
}

.grupo-input input:focus {
  border-color: #555;
}

.botao-entrar {
  background-color: #000;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.botao-entrar:hover {
  background-color: #333;
}
</style>