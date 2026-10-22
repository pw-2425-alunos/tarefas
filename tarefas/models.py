from django.db import models


class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    user = models.CharField(max_length=150)
    prioridade = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.titulo
