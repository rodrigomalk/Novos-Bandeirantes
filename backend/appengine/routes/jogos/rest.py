# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.json_middleware import JsonResponse
from jogo_app import jogo_facade


@login_not_required
def index():
    cmd = jogo_facade.list_jogos_cmd()
    jogo_list = cmd()
    jogo_form = jogo_facade.jogo_form()
    jogo_dcts = [jogo_form.fill_with_model(m) for m in jogo_list]
    return JsonResponse(jogo_dcts)


@login_not_required
def new(_resp, **jogo_properties):
    cmd = jogo_facade.save_jogo_cmd(**jogo_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_not_required
def edit(_resp, id, **jogo_properties):
    cmd = jogo_facade.update_jogo_cmd(id, **jogo_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_not_required
def delete(_resp, id):
    cmd = jogo_facade.delete_jogo_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


@login_not_required
def _save_or_update_json_response(cmd, _resp):
    try:
        jogo = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    jogo_form = jogo_facade.jogo_form()
    return JsonResponse(jogo_form.fill_with_model(jogo))

