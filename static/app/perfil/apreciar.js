define([
  'text!app/perfil/apreciarTemplate.html',
  'app/models/reconhecerViewModel',
  'template',
  'growl',
  'roteador',
  'sessaoDeUsuario',
], function(apreciarTemplate, ReconhecerViewModel, template, growl, roteador, sessaoDeUsuario) {
  'use strict';

  var _self = {};
  var _sandbox;

  _self.inicializar = function(sandbox, colaboradorId) {
    _sandbox = sandbox;
    _sandbox.escutar('exibir-espaco-para-apreciar', exibir);
  };

  _self.finalizar = function() {
  };

  function exibir(colaboradorId, reconhecimentosDoColaborador) {
    if (sessaoDeUsuario.id === colaboradorId)
      return;

    template.exibirEm('div[data-js="apreciacao"]', apreciarTemplate, reconhecimentosDoColaborador);

    $('#conteudo')
      .on('click', 'div.escrever-apreciacao div.campos', selecionarPilar)
      .on('click', 'button[data-js="reconhecer"]', reconhecer);
  }

  function selecionarPilar() {
    $('div.campos.selecionado').removeClass('selecionado');
    $(this).toggleClass('selecionado').find(':radio').attr('checked', true);
  }

  function reconhecer() {
    var reconhecerViewModel = new ReconhecerViewModel();
    validarOperacao(reconhecerViewModel);

    $.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
      growl.deSucesso().exibir('Reconhecimento realizado com sucesso');
      roteador.atualizar();
    });
  }

  function validarOperacao(reconhecerViewModel) {
    if (reconhecerViewModel.situacao === '')
      throw new ViolacaoDeRegra('A situação deve ser informada');

    if (reconhecerViewModel.comportamento === '')
      throw new ViolacaoDeRegra('O comportamento que a pessoa exibiu deve ser informado');

    if (reconhecerViewModel.impacto === '')
      throw new ViolacaoDeRegra('O impacto que isso gerou deve ser informado');
  }

  return _self;
});