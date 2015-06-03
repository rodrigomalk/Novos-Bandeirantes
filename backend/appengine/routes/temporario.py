# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from tekton.gae.middleware.redirect import RedirectResponse

@no_csrf
def editar():
    query=Game.query()
    jogo_lista = query.fetch()
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    editar_form_path=router.to_path(editar_form)
    for jogo in jogo_lista:
        jogo['edit_path']='%s/%s'%(editar_form_path, jogo['id'])
    contexto = {'jogo_lista': jogo_lista}
    return TemplateResponse(contexto)

@login_not_required
@no_csrf
def criar():
    contexto={'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)

@no_csrf
def editar_form(jogo_id):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    jogo_form=GameForm()
    jogo_form.fill_with_model(jogo)
    contexto={'editar_path': router.to_path(atualizar, jogo_id),
              'game' : jogo_form}
    return TemplateResponse(contexto, 'temporario/editar/forme.html')

def atualizar(jogo_id, **propriedades):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'editar_path': router.to_path(atualizar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'temporario/editar/form.html')
    else:
        game_form.fill_model(jogo)
        jogo.put()
        return RedirectResponse(router.to_path(editar))

class Game(ndb.Model):
    tit=ndb.StringProperty(required=True)
    map=ndb.StringProperty(required=True)
    qtd=ndb.IntegerProperty(default=1)
    tmp=ndb.IntegerProperty()
    grup=ndb.StringProperty()

class GameFormTable(ModelForm):
    _model_class = Game

class GameForm(ModelForm):
    _model_class = Game

def salvar(**propriedades):
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'criar_modelo': router.to_path(salvar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'temporario/criar/form.html')
    else:
        jogo=game_form.fill_model()
        jogo.put()
        return RedirectResponse(router.to_path(editar))