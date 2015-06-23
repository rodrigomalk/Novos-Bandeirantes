# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from routes import jogos
from jogo_app import jogo_facade
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
@login_not_required
def index(jogo_id):
    jogo = jogo_facade.get_jogo_cmd(jogo_id)()
    jogo_form = jogo_facade.jogo_form()
    context = {'save_path': router.to_path(save, jogo_id), 'jogo': jogo_form.fill_with_model(jogo)}
    return TemplateResponse(context, 'jogos/jogo_form.html')


@login_not_required
def save(jogo_id, **jogo_properties):
    cmd = jogo_facade.update_jogo_cmd(jogo_id, **jogo_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'jogo': jogo_properties}

        return TemplateResponse(context, 'jogos/jogo_form.html')
    return RedirectResponse(router.to_path(jogos))

