# coding: utf-8

from models import Quest
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse


@no_csrf
def answer_question(answer, tries, quest_id):
    response = {}
    quest = Quest.get_by_id(long(quest_id))
    if quest is None:
        raise Exception("the quest associated with %s doe not exists" % quest_id)
    if quest.answer.lower() == answer.lower():
        response['right'] = True
    else:
        response['right'] = False
    game = quest.jog.get()
    game_dict = game.to_dict()
    if tries < game_dict['qtd']:
        response['can_try_again'] = True
    else:
        response['can_try_again'] = False

    return JsonResponse(response)