# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from gaegraph.model import Node
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm

@login_not_required
@no_csrf
def index():
    contexto={'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)

class Game(Node):
    tit=ndb.StringProperty(required=True)
    map=ndb.StringProperty(required=True)
    grup=ndb.StringProperty()

class GameForm(ModelForm):
    _model_class = Game

def salvar(**propriedades):
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'criar_modelo': router.to_path(salvar)}
            return TemplateResponse(contexto, 'criar/home.html')
    else:
        pass
    jogo=Game(tit=propriedades['tit'], map=propriedades['map'], grup=propriedades['gru'])
    jogo.put()