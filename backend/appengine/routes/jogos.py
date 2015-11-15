# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton.gae.middleware.json_middleware import JsonResponse
from jogo_app import jogo_facade
from gaecookie.decorator import no_csrf


@no_csrf
def index():
    return TemplateResponse(template_path='jogar/home.html')


@no_csrf
def listar_jogos():
    cmd = jogo_facade.list_jogos_cmd()
    jogo_list = cmd()
    jogo_form = jogo_facade.jogo_form()
    jogo_dcts = [jogo_form.fill_with_model(m) for m in jogo_list]
    return JsonResponse(jogo_dcts)