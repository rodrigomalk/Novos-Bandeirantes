# coding: utf-8

from gaeforms.ndb.form import ModelForm
from models import Game, Quest

class GameForm(ModelForm):
    _model_class = Game


class GameFormTable(ModelForm):
    _model_class = Game


class QuestForm(ModelForm):
    _model_class = Quest
