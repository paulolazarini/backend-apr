from django.db import models
from django.contrib.auth.models import User

class ArvorePreRequisitos(models.Model):
    nome_apr = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_apr

class Objetivo(models.Model):
    arvore = models.ForeignKey(ArvorePreRequisitos, on_delete=models.CASCADE)
    nome_objetivo = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_objetivo

class Obstaculo(models.Model):
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE)
    nome_obstaculo = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_obstaculo

class PreRequisito(models.Model):
    # Opções para o campo de prioridade
    class Prioridade(models.IntegerChoices):
        BAIXA = 1, 'Baixa'
        MEDIA = 2, 'Média'
        ALTA = 3, 'Alta'

    obstaculo = models.ForeignKey(Obstaculo, on_delete=models.CASCADE)
    nome_requisito = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(
        choices=Prioridade.choices,
        default=Prioridade.MEDIA
    )

    def __str__(self):
        return self.nome_requisito

class Dependencias(models.Model):
    requisito_origem = models.ForeignKey(
        PreRequisito,
        on_delete=models.CASCADE,
        related_name='dependencias_de_saida'
    )
    requisito_alvo = models.ForeignKey(
        PreRequisito,
        on_delete=models.CASCADE,
        related_name='dependencias_de_entrada'
    )

    class Meta:
        unique_together = ('requisito_origem', 'requisito_alvo')
        verbose_name_plural = "Dependências"

    def __str__(self):
        return f'{self.requisito_origem.nome_requisito} -> {self.requisito_alvo.nome_requisito}'