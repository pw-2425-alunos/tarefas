// Variáveis

const API_URL = 'https://tarefas.pw.deisi.ulusofona.pt'
const ul_node = document.querySelector('ul')

const titulo_node = document.querySelector("#titulo")
const prioridade_node = document.querySelector("#prioridade")
const user_node = document.querySelector("#user")

const titulo_edit_node = document.querySelector("#edit_titulo")
const prioridade_edit_node = document.querySelector("#edit_prioridade")
const user_edit_node = document.querySelector("#edit_user")

const submit_node = document.querySelector("input[type='submit']")
const modal_node = document.querySelector("#modal_editar");

//
// Fetch de dados

function listarTarefas() {
  fetch(`${API_URL}/tarefas`)
    .then(response => {
      if (!response.ok) throw new Error(response.status);
      return response.json();
    })
    .then(data => {
      ul_node.innerHTML = ""
      data.forEach(item =>{
        const li = document.createElement('li')

        const tarefa = document.createElement('span')
        tarefa.innerHTML = `${item.titulo} ${"⭐️".repeat(item.prioridade)} (${item.user})`

        const btn_editar = document.createElement('button');
        btn_editar.innerHTML = '<i class="fa-solid fa-pen-to-square" aria-hidden="true"></i>';

        btn_editar.title = 'Editar tarefa';
        btn_editar.onclick = () => editarTarefa(item.id);

        const btn_apagar = document.createElement('button');
        btn_apagar.innerHTML = '<i class="fa-solid fa-trash" aria-hidden="true"></i>';

        btn_apagar.title = 'Apagar tarefa';
        btn_apagar.onclick = () => apagarTarefa(item.id);

        li.append(tarefa, btn_editar, btn_apagar);

        ul_node.append(li)
      })
    })
    .catch(error => {
      console.error("Erro ao carregar tarefas:", error);
      alert("Não foi possível carregar as tarefas.");
    })
}

//
// Event handlers
function criarTarefa(event) {
  event.preventDefault()

  if (![1, 2, 3].includes(Number(prioridade_node.value))) {
    alert("A prioridade deve ser 1, 2 ou 3.");
    prioridade_node.focus();
    return;
  }

  fetch(`${API_URL}/tarefas`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      titulo: titulo_node.value,
      user: user_node.value,
      prioridade: prioridade_node.value
    })
  })
  .then(response =>  {
    if (!response.ok) throw new Error(response.status);
    
    document.querySelector("form").reset();
    listarTarefas()
  })
  .catch(error => {
    console.error("Erro ao criar tarefa:", error);
    alert("Não foi possível criar a tarefa.");
  });
}

function atualizarTarefa(event) {
  event.preventDefault()

  const id = document.querySelector("#edit_id").value;
  
  fetch(`${API_URL}/tarefas/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      titulo: titulo_edit_node.value,
      user: user_edit_node.value,
      prioridade: prioridade_edit_node.value
    })
  })
  .then(response => {
    if (!response.ok) throw new Error(response.status);
    
    modal_node.close();
    listarTarefas()
  })
  .catch(error => {
    console.error("Erro ao atualizar tarefa:", error);
    alert("Não foi possível atualizar a tarefa.");
  });
}

function apagarTarefa(id) {
  fetch(`${API_URL}/tarefas/${id}`,{
    method: 'DELETE',
  })
  .then(response => {
    if (!response.ok) throw new Error(response.status);
    listarTarefas()
  })
  .catch(error => {
    console.error("Erro ao apagar tarefa:", error);
    alert("Não foi possível apagar a tarefa.");
  });
}

function editarTarefa(id) {

  fetch(`${API_URL}/tarefas/${id}`,{
    method: 'GET',
  })
  .then(response => {
    if (!response.ok) throw new Error(response.status);
    return response.json()
  })
  .then(data => {
    document.querySelector("#edit_id").value = data.id;
    document.querySelector("#edit_titulo").value = data.titulo;
    document.querySelector("#edit_prioridade").value = data.prioridade;
    document.querySelector("#edit_user").value = data.user;

    modal_node.showModal()
  })
  .catch(error => {
    console.error("Erro ao editar a tarefa:", error);
    alert("Não foi possível editar a tarefa.");
  });
}

//
// Event listeners
submit_node.onclick = criarTarefa

document.querySelector("#form_editar")
        .onsubmit = atualizarTarefa

document.querySelector("#fechar_modal")
        .addEventListener('click', () => modal_node.close())

//
// Inicialização
listarTarefas()