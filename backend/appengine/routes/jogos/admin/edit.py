# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from jogo_app import facade
from routes.jogos import admin


@no_csrf
def index(jogo_id):
    jogo = facade.get_jogo_cmd(jogo_id)()
    detail_form = facade.jogo_detail_form()
    context = {'save_path': router.to_path(save, jogo_id), 'jogo': detail_form.fill_with_model(jogo)}
    return TemplateResponse(context, 'jogos/admin/form.html')


def save(_handler, jogo_id, **jogo_properties):
    cmd = facade.update_jogo_cmd(jogo_id, **jogo_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'jogo': cmd.form}

        return TemplateResponse(context, 'jogos/admin/form.html')
    _handler.redirect(router.to_path(admin))

