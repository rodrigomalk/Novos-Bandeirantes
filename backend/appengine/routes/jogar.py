# coding: utf-8

from __future__ import absolute_import, unicode_literals
import json
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse
from models import Quest, Game


@no_csrf
def index(_logged_user, game_id):
    game = Game.get_by_id(long(game_id))
    quests = Quest.query().fetch()
    quest_list = [quest.to_dict(exclude=["jog"]) for quest in quests if quest.jog.id() == game.key.id()]
    dict_ = {
        'game': json.dumps(game.to_dict()),
        'quests': json.dumps(quest_list)
    }
    return TemplateResponse(context=dict_, template_path="jogar/jogar.html")