# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from jogo_app.model import Jogo

class JogoPublicForm(ModelForm):
    """
    Form used to show properties on app's home
    """
    _model_class = Jogo
    _include = [Jogo.tit,
                Jogo.map,
                Jogo.qtd,
                Jogo.tmp,
                Jogo.grp]


class JogoForm(ModelForm):
    """
    Form used to save and update operations on app's admin page
    """
    _model_class = Jogo
    _include = [Jogo.tit,
                Jogo.map,
                Jogo.qtd,
                Jogo.tmp,
                Jogo.grp]


class JogoDetailForm(ModelForm):
    """
    Form used to show entity details on app's admin page
    """
    _model_class = Jogo
    _include = [Jogo.tit,
                Jogo.map,
                Jogo.qtd,
                Jogo.tmp,
                Jogo.grp]


class JogoShortForm(ModelForm):
    """
    Form used to show entity short version on app's admin page, mainly for tables
    """
    _model_class = Jogo
    _include = [Jogo.tit,
                Jogo.map,
                Jogo.qtd,
                Jogo.tmp,
                Jogo.grp]


class SaveJogoCommand(SaveCommand):
    _model_form_class = JogoForm


class UpdateJogoCommand(UpdateNode):
    _model_form_class = JogoForm


class ListJogoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListJogoCommand, self).__init__(Jogo.query_by_creation())

