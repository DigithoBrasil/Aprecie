from django.db import models
from Reconhecimentos.models import Reconhecimento

class Funcionario(models.Model):
	nome = models.CharField(max_length='200')
	cpf = models.CharField(max_length='11', unique=True)
	data_de_nascimento = models.DateField()

	def reconhecer(self, reconhecedor, valor, justificativa):
		if reconhecedor == self:
			raise Exception('O colaborador nao pode reconher a si próprio')

		if not justificativa.strip():
			raise Exception('A sua justificativa deve ser informada')

		Reconhecimento.objects.create(reconhecedor=reconhecedor, funcionario=self, valor=valor, justificativa=justificativa)

	def reconhecimentos(self):
		return Reconhecimento.objects.filter(funcionario=self)

	def reconhecimentos_por_valor(self, valor):
		return self.reconhecimentos().filter(valor=valor)