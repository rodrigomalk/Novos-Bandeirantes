# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from jogo_app import jogo_facade
from gaegraph.model import Arc
from google.appengine.ext import ndb
from jogo_app.jogo_model import Jogo


def index(_logged_user):
    user_key = _logged_user.key
    query = Autor.query(Autor.origin == user_key)
    autores = query.fetch()
    game_keys = [autor.destination for autor in autores]
    jogos = ndb.get_multi(game_keys)
    cmd = jogo_facade.list_jogos_cmd()
    jogo_list = cmd()
    jogo_form = jogo_facade.jogo_form()
    jogo_dcts = [jogo_form.fill_with_model(m) for m in jogo_list if m in jogos]
    return JsonResponse(jogo_dcts)

def new(_resp, _logged_user, **jogo_properties):
    cmd = jogo_facade.save_jogo_cmd(**jogo_properties)
    return _save_or_update_json_response(cmd, _logged_user, _resp)


def edit(_resp, jogo_id, **jogo_properties):
    cmd = jogo_facade.update_jogo_cmd(jogo_id, **jogo_properties)
    return update_json_response(cmd, _resp)


def delete(_resp, jogo_id):
    cmd = jogo_facade.delete_jogo_cmd(jogo_id)
    try:
        cmd()
        chave = ndb.Key(Jogo, int(jogo_id))
        query=Autor.find_origins(chave)
        chaves_autores=query.fetch(keys_only=True)
        ndb.delete_multi(chaves_autores)
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)

def _save_or_update_json_response(cmd, _logged_user, _resp):
    try:
        jogo = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    user_key = _logged_user.key
    autor = Autor(origin=user_key, destination=jogo)
    autor.put()
    jogo_form = jogo_facade.jogo_form()
    return JsonResponse(jogo_form.fill_with_model(jogo))

def update_json_response(cmd, _resp):
    try:
        jogo = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    jogo_form = jogo_facade.jogo_form()
    return JsonResponse(jogo_form.fill_with_model(jogo))

class Autor(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(required=True)
