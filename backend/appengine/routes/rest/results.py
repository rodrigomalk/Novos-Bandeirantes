# coding: utf-8

import json
from models import Game, Result
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse
from gaepermission.decorator import login_required


@no_csrf
@login_required
def add(_logged_user, **kwargs):

    user_key = _logged_user.key
    game_id = kwargs.get("game_id")
    points = kwargs.get("points")
    won_medal = kwargs.get("won_medal")
    duration = kwargs.get('duration')
    size = kwargs.get('size')
    game = Game.get_by_id(long(game_id))
    game_title = game.to_dict()['tit']

    result = Result.change_result_attrs(points=points, won_medal=won_medal, duration=duration,
                                        game_title=game_title, game=game, user_key=user_key, size=size)
    result.put()
    return JsonResponse(json.dumps({}))