# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from jogo_app import jogo_facade


def index():
    cmd = jogo_facade.list_jogos_cmd()
    jogo_list = cmd()
    jogo_form = jogo_facade.jogo_form()
    jogo_dcts = [jogo_form.fill_with_model(m) for m in jogo_list]
    return JsonResponse(jogo_dcts)


def new(_resp, **jogo_properties):
    cmd = jogo_facade.save_jogo_cmd(**jogo_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, jogo_id, **jogo_properties):
    cmd = jogo_facade.update_jogo_cmd(jogo_id, **jogo_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, jogo_id):
    cmd = jogo_facade.delete_jogo_cmd(jogo_id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        jogo = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    jogo_form = jogo_facade.jogo_form()
    return JsonResponse(jogo_form.fill_with_model(jogo))

