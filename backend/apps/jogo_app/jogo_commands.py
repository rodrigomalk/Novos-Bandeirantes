# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from jogo_app.jogo_model import Jogo



class JogoSaveForm(ModelForm):
    """
    Form used to save and update Jogo
    """
    _model_class = Jogo


class JogoForm(ModelForm):
    """
    Form used to expose Jogo's properties for list or json
    """
    _model_class = Jogo


class GetJogoCommand(NodeSearch):
    _model_class = Jogo


class DeleteJogoCommand(DeleteNode):
    _model_class = Jogo


class SaveJogoCommand(SaveCommand):
    _model_form_class = JogoSaveForm


class UpdateJogoCommand(UpdateNode):
    _model_form_class = JogoSaveForm


class ListJogoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListJogoCommand, self).__init__(Jogo.query_by_creation())

