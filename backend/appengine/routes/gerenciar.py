# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from gaecookie.decorator import no_csrf
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_not_required, login_required

from arcos import Autor
from config.template_middleware import TemplateResponse
from forms import GameForm, GameFormTable, QuestForm
from models import Game, Quest
from routes.jogos import download


@no_csrf
@login_required
def index(_logged_user):
    user_key = _logged_user.key
    query = Autor.query(Autor.origin == user_key)
    autores = query.fetch()
    game_keys = [autor.destination for autor in autores]
    jogo_lista = ndb.get_multi(game_keys)
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    editar_form_path = router.to_path(editar_form)
    deletar_form_path = router.to_path(deletar_form)

    success_url = router.to_path(upload)
    pergunta_url = router.to_path(pergunta)
    bucket = get_default_gcs_bucket_name()
    upload_url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
    for jogo in jogo_lista:
        jogo['edit_path'] = '%s/%s' % (editar_form_path, jogo['id'])
        jogo['delete_path'] = '%s/%s' % (deletar_form_path, jogo['id'])
    contexto = {'jogo_lista': jogo_lista, "upload_url": upload_url, "pergunta_url": pergunta_url}
    return TemplateResponse(contexto)


@no_csrf
@login_required
def upload(_handler, **jogos_properties):
    if jogos_properties.get('files'):
        blob_infos = _handler.get_uploads("files[]")
        blob_key = blob_infos[0].key()
        avatar = router.to_path(download, blob_key)
        cmd = Game.get_by_id(long(jogos_properties['id']))
        cmd.foto = avatar
        cmd.put()
        return RedirectResponse(router.to_path(index))


@no_csrf
@login_required
def criar():
    contexto = {'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)


@no_csrf
@login_required
def deletar_form(jogo_id):
    chave = ndb.Key(Game, int(jogo_id))
    chave.delete()
    query = Autor.find_origins(chave)
    chaves_autores = query.fetch(keys_only=True)
    ndb.delete_multi(chaves_autores)
    return RedirectResponse(router.to_path(index))


@no_csrf
@login_required
def editar_form(jogo_id):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    jogo_form = GameForm()
    jogo_form.fill_with_model(jogo)
    contexto = {'editar_path': router.to_path(atualizar, jogo_id),
              'game' : jogo_form}
    return TemplateResponse(contexto, 'temporario/forme.html')


@login_required
def atualizar(jogo_id, **propriedades):
    jogo_id = int(jogo_id)
    jogo = Game.get_by_id(jogo_id)
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto = {'editar_path': router.to_path(atualizar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'temporario/form.html')
    else:
        game_form.fill_model(jogo)
        jogo.put()
        return RedirectResponse(router.to_path(index))


@login_required
def salvar(_logged_user, **propriedades):
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'criar_modelo': router.to_path(salvar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'temporario/criar/form.html')
    else:
        jogo = game_form.fill_model()
        game_key = jogo.put()
        user_key = _logged_user.key
        autor = Autor(origin=user_key, destination=game_key)
        autor.put()
        return RedirectResponse(router.to_path(index))


@no_csrf
@login_required
def pergunta(game_id):
    quest_form = QuestForm()
    quests = [quest_form.fill_with_model(quest) for quest in Quest.query().fetch()]

    return TemplateResponse({"quests": quests, "game_id": game_id}, template_path="gerenciar/pergunta.html")


