# coding: utf-8

from gaegraph.model import Node
from google.appengine.ext import ndb

class Game(Node):
    tit=ndb.StringProperty(required=True)
    map=ndb.StringProperty(required=True)
    grup=ndb.StringProperty()


class Quest(ndb.Model):
	question=ndb.StringProperty(required=True)
	answer=ndb.StringProperty(required=True)
	jog=ndb.KeyProperty()