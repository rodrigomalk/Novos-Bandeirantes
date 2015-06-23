# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from jogo_app import facade
from routes.jogos.admin import new, edit


def delete(_handler, jogo_id):
    facade.delete_jogo_cmd(jogo_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    cmd = facade.list_jogos_cmd()
    jogos = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    short_form = facade.jogo_short_form()

    def short_jogo_dict(jogo):
        jogo_dct = short_form.fill_with_model(jogo)
        jogo_dct['edit_path'] = router.to_path(edit_path, jogo_dct['id'])
        jogo_dct['delete_path'] = router.to_path(delete_path, jogo_dct['id'])
        return jogo_dct

    short_jogos = [short_jogo_dict(jogo) for jogo in jogos]
    context = {'jogos': short_jogos,
               'new_path': router.to_path(new)}
    return TemplateResponse(context)

