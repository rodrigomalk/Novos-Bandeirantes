# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from tekton.gae.middleware.redirect import RedirectResponse

@login_not_required
@no_csrf
def index():
    contexto={'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)

class Game(ndb.Model):
    tit=ndb.StringProperty(required=True)
    map=ndb.StringProperty(required=True)
    qtd=ndb.IntegerProperty(default=1)
    tmp=ndb.IntegerProperty()
    grup=ndb.StringProperty()

titulo = ''

class GameForm(ModelForm):
    _model_class = Game

def salvar(**propriedades):
    global titulo
    game_form = GameForm(**propriedades)
    titulo = propriedades['tit']
    erros = game_form.validate()
    if erros:
            contexto={'criar_modelo': router.to_path(salvar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'criar/form.html')
    else:
        jogo=game_form.fill_model()
        jogo.put()
        return RedirectResponse(router.to_path(continuar))

@login_not_required
@no_csrf
def continuar():
    ctx={'criar_jogo': router.to_path(inserir)}
    return TemplateResponse(ctx, "/criar/criando.html")

class Quest(ndb.Model):
    perg=ndb.StringProperty(required=True)
    resp=ndb.StringProperty(required=True)
    jog=ndb.KeyProperty()

class QuestForm(ModelForm):
    _model_class = Quest

def inserir(**propriedades):
    quest_form = QuestForm(**propriedades)
    #jogo = Game.query(Game.tit == titulo)
    #jogos = jogo.fetch()
    #for j in jogos:
    #    quest_form.jog = j.key.id
    erro = quest_form.validate()
    if erro:
            contexto={'criar_modelo': router.to_path(salvar),
                      'quest': quest_form,
                      'erro': erro}
            return TemplateResponse(contexto, 'criar/criandoform.html')
    else:
        questao=quest_form.fill_model()
        questao.put()
        return RedirectResponse(router.to_path(continuar))