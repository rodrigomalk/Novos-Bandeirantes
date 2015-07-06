# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from tekton import router
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Arc
from tekton.gae.middleware.redirect import RedirectResponse

@no_csrf
def index(_logged_user):
    user_key = _logged_user.key
    query = Autor.query(Autor.origin == user_key)
    autores = query.fetch()
    game_keys = [autor.destination for autor in autores]
    jogo_lista = ndb.get_multi(game_keys)
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    editar_form_path=router.to_path(editar_form)
    deletar_form_path=router.to_path(deletar_form)
    for jogo in jogo_lista:
        jogo['edit_path']='%s/%s'%(editar_form_path, jogo['id'])
        jogo['delete_path']='%s/%s'%(deletar_form_path, jogo['id'])
    contexto = {'jogo_lista': jogo_lista}
    return TemplateResponse(contexto)

@no_csrf
def jogar():
    query=Game.query()
    jogo_lista = query.fetch()
    form = GameFormTable()
    jogo_lista = [form.fill_with_model(jogo) for jogo in jogo_lista]
    contexto = {'jogo_lista': jogo_lista}
    return TemplateResponse(contexto)

@no_csrf
def criar():
    contexto={'criar_modelo': router.to_path(salvar)}
    return TemplateResponse(contexto)

@no_csrf
def deletar_form(jogo_id):
    chave = ndb.Key(Game, int(jogo_id))
    chave.delete()
    query=Autor.find_origins(chave)
    chaves_autores=query.fetch(keys_only=True)
    ndb.delete_multi(chaves_autores)
    return RedirectResponse(router.to_path(index))

@no_csrf
def editar_form(jogo_id):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    jogo_form=GameForm()
    jogo_form.fill_with_model(jogo)
    contexto={'editar_path': router.to_path(atualizar, jogo_id),
              'game' : jogo_form}
    return TemplateResponse(contexto, 'temporario/forme.html')

def atualizar(jogo_id, **propriedades):
    jogo_id = int(jogo_id)
    jogo=Game.get_by_id(jogo_id)
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'editar_path': router.to_path(atualizar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'temporario/form.html')
    else:
        game_form.fill_model(jogo)
        jogo.put()
        return RedirectResponse(router.to_path(index))

def salvar(_logged_user, **propriedades):
    game_form = GameForm(**propriedades)
    erros = game_form.validate()
    if erros:
            contexto={'criar_modelo': router.to_path(salvar),
                      'game': game_form,
                      'erros': erros}
            return TemplateResponse(contexto, 'temporario/criar/form.html')
    else:
        jogo=game_form.fill_model()
        game_key = jogo.put()
        user_key = _logged_user.key
        autor = Autor(origin=user_key, destination=game_key)
        autor.put()
        return RedirectResponse(router.to_path(index))


class Game(ndb.Model):
    tit=ndb.StringProperty(required=True)
    map=ndb.StringProperty(required=True)
    qtd=ndb.IntegerProperty(default=1)
    tmp=ndb.IntegerProperty(default=0)
    grup=ndb.StringProperty()

class GameForm(ModelForm):
    _model_class = Game

class GameFormTable(ModelForm):
    _model_class = Game

class Autor(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Game, required=True)