import logging
from typing import List

from ninja import Field, ModelSchema, NinjaAPI, Schema
from ninja.errors import HttpError, ValidationError
from project import settings

from .models import Tarefa

logger = logging.getLogger(__name__)

api = NinjaAPI(
    title="Tarefas API",
    servers=(
        [{"url": "https://tarefas.pw.deisi.ulusofona.pt"}]
        if not settings.DEBUG
        else [{"url": "/", "description": "Servidor de Desenvolvimento"}]
    )
)


class TarefaIn(Schema):
    titulo: str = Field(..., min_length=1, max_length=200)
    user: str = Field(..., min_length=1, max_length=150)
    prioridade: int = Field(1, ge=1, le=3)


class TarefaOut(ModelSchema):
    class Meta:
        model = Tarefa
        fields = ["id", "titulo", "user", "prioridade"]



class ErroOut(Schema):
    detail: str


class ErroCampoOut(Schema):
    campo: str
    mensagem: str


class ErroValidacaoOut(Schema):
    detail: str
    erros: List[ErroCampoOut]


TAG = ["Tarefas"]
NAO_ENCONTRADA = {"detail": "Tarefa não encontrada."}

ERROS_COMUNS = {405: ErroOut, 500: ErroOut}
ERROS_ID = {404: ErroOut, 422: ErroValidacaoOut, **ERROS_COMUNS}
ERROS_CORPO = {400: ErroOut, 422: ErroValidacaoOut, **ERROS_COMUNS}

MENSAGENS = {
    "missing": "Campo obrigatório.",
    "string_type": "Deve ser texto.",
    "int_type": "Deve ser um número inteiro.",
    "int_parsing": "Deve ser um número inteiro.",
    "string_too_short": "Deve ter pelo menos {min_length} carater(es).",
    "string_too_long": "Deve ter no máximo {max_length} carateres.",
    "greater_than_equal": "Deve ser maior ou igual a {ge}.",
    "less_than_equal": "Deve ser menor ou igual a {le}.",
}


def _mensagem(erro: dict) -> str:
    modelo = MENSAGENS.get(erro.get("type"))
    if modelo is None:
        return erro.get("msg", "Valor inválido.")
    return modelo.format(**erro.get("ctx", {}))


@api.exception_handler(ValidationError)
def erro_validacao(request, exc: ValidationError):
    erros = [
        {
            "campo": ".".join(
                str(parte) for parte in e["loc"][1:] if parte != "payload"
            )
            or str(e["loc"][0]),
            "mensagem": _mensagem(e),
        }
        for e in exc.errors
    ]
    return api.create_response(
        request, {"detail": "Dados inválidos.", "erros": erros}, status=422
    )


@api.exception_handler(HttpError)
def erro_http(request, exc: HttpError):
    detail = (
        "Corpo do pedido inválido: JSON mal formado."
        if exc.status_code == 400
        else exc.message
    )
    return api.create_response(request, {"detail": detail}, status=exc.status_code)


@api.exception_handler(Exception)
def erro_interno(request, exc: Exception):
    logger.exception("Erro interno em %s", request.path)
    return api.create_response(
        request, {"detail": "Erro interno do servidor."}, status=500
    )


@api.get("/tarefas", response={200: List[TarefaOut], **ERROS_COMUNS}, tags=TAG)
def listar_tarefas(request):
    return 200, Tarefa.objects.all()


@api.post("/tarefas", response={201: TarefaOut, **ERROS_CORPO}, tags=TAG)
def criar_tarefa(request, payload: TarefaIn):
    return 201, Tarefa.objects.create(**payload.dict())


@api.get("/tarefas/{tarefa_id}", response={200: TarefaOut, **ERROS_ID}, tags=TAG)
def obter_tarefa(request, tarefa_id: int):
    tarefa = Tarefa.objects.filter(id=tarefa_id).first()
    if tarefa is None:
        return 404, NAO_ENCONTRADA
    return 200, tarefa


@api.put(
    "/tarefas/{tarefa_id}",
    response={200: TarefaOut, **ERROS_ID, 400: ErroOut},
    tags=TAG,
)
def alterar_tarefa(request, tarefa_id: int, payload: TarefaIn):
    tarefa = Tarefa.objects.filter(id=tarefa_id).first()
    if tarefa is None:
        return 404, NAO_ENCONTRADA
    for campo, valor in payload.dict().items():
        setattr(tarefa, campo, valor)
    tarefa.save()
    return 200, tarefa


@api.delete("/tarefas/{tarefa_id}", response={204: None, **ERROS_ID}, tags=TAG)
def apagar_tarefa(request, tarefa_id: int):
    tarefa = Tarefa.objects.filter(id=tarefa_id).first()
    if tarefa is None:
        return 404, NAO_ENCONTRADA
    tarefa.delete()
    return 204, None
