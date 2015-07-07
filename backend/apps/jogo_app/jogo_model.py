# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node


class Jogo(Node):
    tit = ndb.StringProperty(required=True)
    map = ndb.StringProperty(required=True)
    qtd = ndb.IntegerProperty(default=1)
    tmp = ndb.IntegerProperty(default=0)
    grp = ndb.StringProperty(default='Jogo Aberto')
    foto = ndb.StringProperty(required=False)

