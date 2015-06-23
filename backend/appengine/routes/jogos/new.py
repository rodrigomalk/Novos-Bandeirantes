# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from jogo_app import jogo_facade
from routes import jogos
from tekton.gae.middleware.redirect import RedirectResponse
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext import blobstore
from jogo_app.jogo_model import Jogo
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, permissions
from config.template_middleware import TemplateResponse
from permission_app.model import ALL_PERMISSIONS_LIST
from routes.jogos import upload
from routes.jogos.upload import edit, delete
from tekton import router


@login_not_required
@no_csrf
def index():
    context = {}
    context["jogo"] = Jogo()
    # gera url para save
    success_url = router.to_path(upload)
    context["groups"] = []
    context["choice_groups"] = ALL_PERMISSIONS_LIST
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
    context["upload_url"] = url
    context["nav_active"] = 'jogos'
    return TemplateResponse(context, template_path='/jogos/jogo_form.html')

@login_not_required
def save(jogo_id, **jogo_properties):
    cmd = jogo_facade.update_jogo_cmd(jogo_id, **jogo_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'jogo': jogo_properties}

        return TemplateResponse(context, 'jogos/jogo_form.html')
    return RedirectResponse(router.to_path(jogos))