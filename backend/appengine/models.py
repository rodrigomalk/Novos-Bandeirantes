# coding: utf-8

from gaegraph.model import Node
from google.appengine.ext import ndb
from datetime import date


class Game(Node):
    tit = ndb.StringProperty(required=True)
    map = ndb.StringProperty(required=True)
    qtd = ndb.IntegerProperty(default=1)
    tmp = ndb.IntegerProperty(default=0)
    grp = ndb.StringProperty(default='Jogo Aberto')
    foto = ndb.StringProperty(required=False)


class Quest(ndb.Model):
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty(required=True)
    jog = ndb.KeyProperty()

    def to_dict(self, *args, **kwargs):
        dict_ = super(Quest, self).to_dict(*args, **kwargs)
        dict_["id"] = self.key.id()
        return dict_


class Result(ndb.Model):
    user = ndb.KeyProperty(required=True)
    game = ndb.KeyProperty(required=True)
    game_title = ndb.StringProperty(required=True)
    last_date = ndb.DateProperty(auto_now=True)
    best_date = ndb.DateProperty()
    last_duration = ndb.FloatProperty()
    medal_date = ndb.DateProperty()
    best_duration = ndb.FloatProperty(default=0.0)
    last_points = ndb.IntegerProperty(default=0)
    best_points = ndb.IntegerProperty(default=0)
    won_medal = ndb.BooleanProperty(default=False)
    frequency = ndb.IntegerProperty(default=0)
    size = ndb.IntegerProperty()

    @classmethod
    def update_many(cls, results):
        return ndb.put_multi(results)

    @classmethod
    def change_result_attrs(cls, **kwargs):

        user_key = kwargs.get("user_key")
        game = kwargs.get('game')
        points = kwargs.get('points')
        game_title  = kwargs.get("game_title")
        won_medal = kwargs.get("won_medal")
        duration  = kwargs.get("duration")
        size = kwargs.get('size')

        result = cls.query(cls.user==user_key, cls.game==game.key).get()
        if result is not None:
            if points > result.best_points:
                result.best_points = points
                result.best_date = date.today()
            if result.best_duration is not None and duration < result.best_duration:
                result.best_duration = duration
            else:
                result.best_duration = duration
        else:
            result = cls(user=user_key, game=game.key, game_title=game_title,
                         best_points=points, best_date=date.today(), best_duration=duration, size=size)

        result.last_points = points
        result.last_duration = duration
        result.frequency += 1
        result.won_medal = won_medal
        if won_medal:
            result.medal_date = date.today()
        return result
