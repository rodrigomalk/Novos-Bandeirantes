# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.criar import Game

@no_csrf
def index():
    query=Game.query()
    contexto = {'jogo_lista':query.fetch}
    return TemplateResponse(contexto)