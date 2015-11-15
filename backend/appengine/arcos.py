from google.appengine.ext import ndb

from models import Game
from gaegraph.model import Arc

class Autor(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Game, required=True)