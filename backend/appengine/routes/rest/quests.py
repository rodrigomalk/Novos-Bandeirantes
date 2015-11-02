# coding: utf-8

import json
from models import Game, Quest
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse


@no_csrf
def all(game_id):
    game = Game.get_by_id(long(game_id))
    if game is not None:
        quests = Quest.query(Quest.jog==game.key).fetch()
        return JsonResponse([quest.to_dict(exclude=["jog"]) for quest in quests])
    raise Exception("game id: %s not found" % game_id)


@no_csrf
def add(question, answer, game_id, id=None):
    game = Game.get_by_id(long(game_id))

    if game is None:
        raise Exception("game id: %s not found" % game_id)
    if id is not None:
        quest = Quest.get_by_id(long(id))
        quest.answer = answer
        quest.question = question
        quest_key = quest.put()
    else:
        quest_key = Quest(question=question, answer=answer, jog=game.key).put()

    return json.dumps({"quest_id": quest_key.id()})


@no_csrf
def delete(quest_id):
    quest = Quest.get_by_id(long(quest_id))
    if quest is not None:
        quest.key.delete()
        return json.dumps({})
    raise Exception("quest id: %s not found" % quest_id)

