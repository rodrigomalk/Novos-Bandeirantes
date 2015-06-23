# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from jogo_app import facade
from routes.jogos import admin


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)},'jogos/admin/form.html')


def save(_handler, jogo_id=None, **jogo_properties):
    cmd = facade.save_jogo_cmd(**jogo_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'jogo': cmd.form}

        return TemplateResponse(context, 'jogos/admin/form.html')
    _handler.redirect(router.to_path(admin))

