# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from arcos import Autor
from forms import GameFormTable
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from models import Result

@no_csrf
@login_required
def index(_logged_user):
    user_key = _logged_user.key
    query = Result.query(Result.user == user_key)
    results = query.fetch()
    resp = "---"
    query = Autor.query()
    autores = query.fetch()
    game_keys = [autor.destination for autor in autores]
    games = ndb.get_multi(game_keys)
    resps = []
    for game in games:
        for result in results:
            if game.key == result.game:
                if result.won_medal is True:
                    resp = "medal"
                else:
                    resp = "%d / %d" % (result.best_points, result.size)
        resps.append(resp)
        resp = "---"
    jogo_lista = []
    for game, result in zip(games, resps):
        game_dict = game.to_dict()
        game_dict['result'] = result
        jogo_lista.append(game_dict)
    return TemplateResponse({"games": jogo_lista}, 'jogos/home.html')
