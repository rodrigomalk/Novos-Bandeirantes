# coding: utf-8

from gaegraph.model import Node
from google.appengine.ext import ndb


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
    date_f = ndb.DateProperty()
    date_l = ndb.DateProperty()
    date_b = ndb.DateProperty()
    first = ndb.IntegerProperty()
    last = ndb.IntegerProperty()
    best = ndb.IntegerProperty()
    medal = ndb.BooleanProperty(default=False)
    qtd = ndb.IntegerProperty(default = 0)