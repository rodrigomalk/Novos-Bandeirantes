# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from models import Game, Quest
from forms import GameForm, QuestForm


@login_not_required
@no_csrf
def index():
    contexto = {'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)

titulo = ''


def salvar(**propriedades):
    global titulo
    game_form = GameForm(**propriedades)
    titulo = propriedades['tit']
    erros = game_form.validate()
    if erros:
            contexto = {'criar_modelo': router.to_path(salvar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'criar/form.html')
    else:
        jogo = game_form.fill_model()
        jogo.put()
        return RedirectResponse(router.to_path(continuar))

@login_not_required
@no_csrf
def continuar():
    ctx = {'criar_jogo': router.to_path(inserir)}
    return TemplateResponse(ctx, "/criar/criando.html")


def inserir(**propriedades):
    quest_form = QuestForm(**propriedades)
    erro = quest_form.validate()
    if erro:
            contexto={'criar_modelo': router.to_path(salvar),
                      'quest': quest_form,
                      'erro': erro}
            return TemplateResponse(contexto, 'criar/criandoform.html')
    else:
        questao = Quest(**propriedades)
        query = Game.query(Game.tit == titulo)
        if query is not None:
            jogos = query.fetch()
        for j in jogos:
            questao.jog.append(j.key)
        questao.put()
        return RedirectResponse(router.to_path(continuar))
