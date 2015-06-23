# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from jogo_app.commands import ListJogoCommand, SaveJogoCommand, UpdateJogoCommand, \
    JogoPublicForm, JogoDetailForm, JogoShortForm


def save_jogo_cmd(**jogo_properties):
    """
    Command to save Jogo entity
    :param jogo_properties: a dict of properties to save on model
    :return: a Command that save Jogo, validating and localizing properties received as strings
    """
    return SaveJogoCommand(**jogo_properties)


def update_jogo_cmd(jogo_id, **jogo_properties):
    """
    Command to update Jogo entity with id equals 'jogo_id'
    :param jogo_properties: a dict of properties to update model
    :return: a Command that update Jogo, validating and localizing properties received as strings
    """
    return UpdateJogoCommand(jogo_id, **jogo_properties)


def list_jogos_cmd():
    """
    Command to list Jogo entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListJogoCommand()


def jogo_detail_form(**kwargs):
    """
    Function to get Jogo's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return JogoDetailForm(**kwargs)


def jogo_short_form(**kwargs):
    """
    Function to get Jogo's short form. just a subset of jogo's properties
    :param kwargs: form properties
    :return: Form
    """
    return JogoShortForm(**kwargs)

def jogo_public_form(**kwargs):
    """
    Function to get Jogo'spublic form. just a subset of jogo's properties
    :param kwargs: form properties
    :return: Form
    """
    return JogoPublicForm(**kwargs)


def get_jogo_cmd(jogo_id):
    """
    Find jogo by her id
    :param jogo_id: the jogo id
    :return: Command
    """
    return NodeSearch(jogo_id)


def delete_jogo_cmd(jogo_id):
    """
    Construct a command to delete a Jogo
    :param jogo_id: jogo's id
    :return: Command
    """
    return DeleteNode(jogo_id)

