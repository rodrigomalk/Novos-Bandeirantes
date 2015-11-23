import json
from models import Game, Result
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse

@no_csrf
def add(_logged_user, points, date, medal, game_id, id=None):
    user_key = _logged_user.key
    game_key = game_id.key
    query = Result.query(Result.user == user_key and Result.game == game_key)
    result = query.fetch()

    if len(result) > 0:
        result = Result.get_by_id(long(id))
        result.last = points
        result.date_l = date
        if points > result.best:
            result.best = points
            result.date_b = date
        if medal:
            result.medal = medal
        result.qtd += 1
        result_key = result.put()
    else:
        result_key = Result(game = game_key, user = user_key, name = game_id.tit, first = points, date_f = date, last = points, date_l = date, best = points, date_b = date, medal = medal, qtd = 1).put()

    return json.dumps({"result_id": result_key.id()})