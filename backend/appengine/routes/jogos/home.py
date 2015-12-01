# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from arcos import Autor
from forms import GameFormTable
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf

@no_csrf
def index():
    query = Autor.query()
    autores = query.fetch()
    game_keys = [autor.destination for autor in autores]
    jogo_lista = ndb.get_multi(game_keys)
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    return TemplateResponse({"games": jogo_lista}, 'jogos/home.html')
