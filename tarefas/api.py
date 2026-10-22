from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, NinjaAPI, Schema

from .models import Tarefa

api = NinjaAPI(title="Tarefas API")


class TarefaIn(Schema):
    titulo: str
    user: str
    prioridade: int = 1


class TarefaOut(ModelSchema):
    class Meta:
        model = Tarefa
        fields = ["id", "titulo", "user", "prioridade"]


@api.post("/tarefas", response={201: TarefaOut})
def criar_tarefa(request, payload: TarefaIn):
    return 201, Tarefa.objects.create(**payload.dict())


@api.get("/tarefas", response=List[TarefaOut])
def listar_tarefas(request):
    return Tarefa.objects.all()


@api.get("/tarefas/{tarefa_id}", response=TarefaOut)
def obter_tarefa(request, tarefa_id: int):
    return get_object_or_404(Tarefa, id=tarefa_id)


@api.put("/tarefas/{tarefa_id}", response=TarefaOut)
def alterar_tarefa(request, tarefa_id: int, payload: TarefaIn):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    for campo, valor in payload.dict().items():
        setattr(tarefa, campo, valor)
    tarefa.save()
    return tarefa


@api.delete("/tarefas/{tarefa_id}", response={204: None})
def apagar_tarefa(request, tarefa_id: int):
    get_object_or_404(Tarefa, id=tarefa_id).delete()
    return 204, None
