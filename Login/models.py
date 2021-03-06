﻿from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from Aprecie.base import ExcecaoDeDominio

class Colaborador(AbstractBaseUser):
  cpf = models.CharField(max_length=11, unique=True)
  nome = models.CharField(max_length=200)
  data_de_nascimento = models.DateField()
  foto = models.TextField(default=None, null=True)
  usuario_no_slack = models.CharField(max_length=100, null=True)

  USERNAME_FIELD = 'cpf'

  @property 
  def primeiro_nome(self):
    return Colaborador.obter_primeiro_nome(self.nome)

  @property
  def nome_abreviado(self):
    return Colaborador.obter_primeiro_nome(self.nome) + ' ' + Colaborador.obter_ultimo_nome(self.nome)

  @staticmethod
  def obter_primeiro_nome(nome):
    return nome.split(' ')[0]

  @staticmethod
  def obter_ultimo_nome(nome):
    return nome.split(' ')[-1]

  def alterar_foto(self, nova_foto_em_base64):
    if not nova_foto_em_base64.strip():
      raise ExcecaoDeDominio('Foto deve ser informada')
      
    self.foto = nova_foto_em_base64

  def reconhecer(self, reconhecedor, pilar, feedback):
    if reconhecedor == self:
      raise ExcecaoDeDominio('O colaborador nao pode reconher a si próprio')

    if not feedback:
      raise ExcecaoDeDominio('Feedback deve ser informado')

    if self.ja_possui_um_reconhecimento_identico(reconhecedor, feedback, pilar):
      raise ExcecaoDeDominio('Não é possível reconhecer uma pessoa duas vezes pelos mesmos motivos')

    self.reconhecido.create(reconhecedor = reconhecedor, pilar = pilar, feedback = feedback)

  def ja_possui_um_reconhecimento_identico(self, reconhecedor, feedback, pilar):
    return self.reconhecido.filter(
        reconhecedor = reconhecedor,
        pilar = pilar,
        feedback__situacao = feedback.situacao,
        feedback__comportamento = feedback.comportamento,
        feedback__impacto = feedback.impacto
      ).exists()

  def reconhecimentos(self):
    return self.reconhecido.all()

  def reconhecimentos_por_pilar(self, pilar):
    return self.reconhecido.filter(pilar = pilar).order_by('-data')
