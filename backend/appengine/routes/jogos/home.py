# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from jogo_app import jogo_facade
from routes.jogos import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
@login_not_required
def index():
    cmd = jogo_facade.list_jogos_cmd()
    jogos = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    jogo_form = jogo_facade.jogo_form()

    def localize_jogo(jogo):
        jogo_dct = jogo_form.fill_with_model(jogo)
        jogo_dct['edit_path'] = router.to_path(edit_path, jogo_dct['id'])
        jogo_dct['delete_path'] = router.to_path(delete_path, jogo_dct['id'])
        return jogo_dct

    localized_jogos = [localize_jogo(jogo) for jogo in jogos]
    context = {'jogos': localized_jogos,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'jogos/jogo_home.html')

@login_not_required
def delete(jogo_id):
    jogo_facade.delete_jogo_cmd(jogo_id)()
    return RedirectResponse(router.to_path(index))

