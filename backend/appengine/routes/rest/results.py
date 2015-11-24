# coding: utf-8
import json
from google.appengine.ext import ndb
from models import Game, Result
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse


@no_csrf
def add(_logged_user, results, game_id):
    """
    results eh uma lista de dicionarios.
    Cada dicionario possui:             
            points: points
            date: dia atual
            medal: medal
    """
    user_key = _logged_user.key
    game = Game.get_by_id(long(game_id))
    results_to_save = []

    # para cada result cria um novo objeto no Result
    # e adiciona na lista de resulst pra salvar
    for result in results:
        points = result.get("points")
        medal = result.get("medal")
        results_to_save.append(Result(last=points, first=points, medal=medal, game=game.key, user=user_key, game_title=game.tit))
        # result.date_l = date
        # if points > result.best:
        #     result.best = points
        #     result.date_b = date
        # if medal:
        #     result.medal = medal
        # result.qtd += 1
        # result_key = result.put()
    ndb.put_multi(results_to_save) # salva todos os resultados daquele jogo 