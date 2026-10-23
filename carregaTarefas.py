tarefas = [
  {
    "titulo": "Criar um jogo simples para jogar com os amigos",
    "user": "diogo",
    "prioridade": 2
  },
  {
    "titulo": "Experimentar uma linguagem de programação nova",
    "user": "ines",
    "prioridade": 2
  },
  {
    "titulo": "Organizar uma noite de jogos com os amigos",
    "user": "miguel",
    "prioridade": 3
  },
  {
    "titulo": "Fazer um treino completo no ginásio",
    "user": "diogo",
    "prioridade": 2
  },
  {
    "titulo": "Aprender a cozinhar um prato digno de chef",
    "user": "ines",
    "prioridade": 3
  },
  {
    "titulo": "Criar uma aplicação para organizar a vida universitária",
    "user": "miguel",
    "prioridade": 1
  },
  {
    "titulo": "Explorar um sítio novo com os amigos",
    "user": "diogo",
    "prioridade": 3
  },
  {
    "titulo": "Participar num hackathon universitário",
    "user": "ines",
    "prioridade": 2
  },
  {
    "titulo": "Fazer uma caminhada e ver o pôr do sol",
    "user": "miguel",
    "prioridade": 3
  },
  {
    "titulo": "Aprender três truques de magia ou cartas",
    "user": "diogo",
    "prioridade": 3
  },
  {
    "titulo": "Atualizar o GitHub com um projeto pessoal",
    "user": "ines",
    "prioridade": 2
  },
  {
    "titulo": "Organizar uma viagem low-cost para um fim de semana",
    "user": "miguel",
    "prioridade": 2
  },
  {
    "titulo": "Passar um dia inteiro a fotografar momentos aleatórios",
    "user": "diogo",
    "prioridade": 3
  },
  {
    "titulo": "Aprender uma música nova na guitarra ou piano",
    "user": "ines",
    "prioridade": 3
  },
  {
    "titulo": "Experimentar um desporto que nunca pratiquei",
    "user": "miguel",
    "prioridade": 2
  },
  {
    "titulo": "Fazer uma maratona de filmes com snacks caseiros",
    "user": "diogo",
    "prioridade": 3
  },
  {
    "titulo": "Criar um bot de Discord para o grupo de amigos",
    "user": "ines",
    "prioridade": 2
  },
  {
    "titulo": "Conhecer pessoas novas num evento universitário",
    "user": "miguel",
    "prioridade": 2
  },
  {
    "titulo": "Passar 24 horas sem redes sociais",
    "user": "diogo",
    "prioridade": 3
  },
  {
    "titulo": "Fazer uma lista de 10 experiências para viver antes dos 21",
    "user": "ines",
    "prioridade": 1
  }
]


from tarefas.models import Tarefa

for t in tarefas:
    Tarefa.objects.create(
        titulo = t["titulo"],
        user = t["user"],
        prioridade = t["prioridade"]
    )