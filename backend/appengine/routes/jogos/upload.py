# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from time import sleep
from jogo_app import jogo_facade
from jogo_app.jogo_model import Jogo
from gaebusiness.business import CommandExecutionException
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, login_required
from routes import jogos
from routes.jogos import download
from tekton import router
from tekton.router import to_path
from tekton.gae.middleware.redirect import RedirectResponse
from google.appengine.ext import blobstore
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name


@no_csrf
@login_required
def index(_handler, **jogos_properties):
    if jogos_properties.get('files'):
        blob_infos = _handler.get_uploads("files[]")
        blob_key = blob_infos[0].key()
        avatar = to_path(download, blob_key)
        jogos_properties['foto'] = avatar
        jogos_properties.pop("files", None)
    try:
        cmd = Jogo(**jogos_properties)
        cmd.put()
    except CommandExecutionException:
        context = {
            'errors': {}
        }
        return TemplateResponse(context, template_path='/jogos/jogo.html')
    sleep(0.5)
    return RedirectResponse(router.to_path(jogos))


@login_required
@no_csrf
def edit(_handler, **jogos_properties):
    if jogos_properties.get('files'):
        blob_infos = _handler.get_uploads("files[]")
        blob_key = blob_infos[0].key()
        avatar = to_path(download, blob_key)
        jogos_properties['avatar'] = avatar
        jogos_properties.pop("files", None)
    obj_id = jogos_properties.pop("key_id", None)
    if not isinstance(jogos_properties.get('groups'), list):
        jogos_properties['groups'] = [jogos_properties.get('groups')]
    # cmd = jogo_facade.update_jogo_cmd(obj_id, **jogos_properties)
    try:
        cmd = Jogo(**jogos_properties)
        cmd.put()
    except CommandExecutionException:
        success_url = router.to_path(edit)
        bucket = get_default_gcs_bucket_name()
        url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
        context = {'errors': {},
                   'upload_url': url,
                   'jogo': jogos_properties}
        return TemplateResponse(context, template_path='/jogos/jogo.html')
    sleep(0.5)
    return RedirectResponse(router.to_path(jogos))


@login_required
@no_csrf
def delete(obj_id=0):
    cmd = jogo_facade.delete_jogo_cmd(obj_id)
    try:
        cmd()
    except CommandExecutionException:
        return TemplateResponse({}, template_path='/jogos/jogo.html')
    sleep(0.5)
    return RedirectResponse(router.to_path(jogos))