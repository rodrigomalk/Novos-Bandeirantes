# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from gaeforms.ndb.form import ModelForm
from routes.criar import Game
from routes.criar import GameForm

@no_csrf
def index():
    query=Game.query()
    jogo_lista = query.fetch()
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    form_path=router.to_path(form)
    for jogo in jogo_lista:
        jogo['edit_path']='%s/%s'%(form_path, jogo['id'])
    contexto = {'jogo_lista': jogo_lista}
    return TemplateResponse(contexto)

@no_csrf
def form(jogo_id):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    jogo_form=GameForm()
    jogo_form.fill_with_model(jogo)
    contexto={'salvar_path': router.to_path(salvar, jogo_id),
              'jogo':jogo_form}
    return TemplateResponse(contexto, 'editar/form.html')

class GameFormTable(ModelForm):
    _model_class = Game

def salvar(jogo_id, **propriedades):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'criar_modelo': router.to_path(salvar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'editar/form.html')
    else:
        game_form.fill_model(jogo)
        jogo.put()
        # RedirectResponse(router.to_path(continuar))