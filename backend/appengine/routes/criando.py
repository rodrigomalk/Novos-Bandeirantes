# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from google.appengine.ext import ndb
from forms import GameForm
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    contexto={'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)

def salvar(**propriedades):
    game_form = GameForm(**propriedades)
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
    ctx={'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(ctx, "../criando")