# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from arcos import Autor
from forms import GameFormTable
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from models import Result

@no_csrf
def index(_logged_user):
    user_key = _logged_user.key
    query = Result.query(Result.user == user_key)
    results = query.fetch()
    resp = "---"
    query = Autor.query()
    autores = query.fetch()
    game_keys = [autor.destination for autor in autores]
    jogo_lista = ndb.get_multi(game_keys)
    for game in jogo_lista:
        for result in results:
            if game.key == result.game:
                if result.won_medal is True:
                    resp = "medal"
                else:
                    resp = "%d / %d" % (result.best_points, result.size)
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    return TemplateResponse({"games": jogo_lista, "resp": resp}, 'jogos/home.html')
