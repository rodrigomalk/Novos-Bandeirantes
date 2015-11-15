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