# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from jogo_app.jogo_model import Jogo
from routes.jogos.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        jogo = mommy.save_one(Jogo)
        template_response = index(jogo.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        jogo = mommy.save_one(Jogo)
        old_properties = jogo.to_dict()
        redirect_response = save(jogo.key.id(), foto='foto_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_jogo = jogo.key.get()
        self.assertEquals('foto_string', edited_jogo.foto)
        self.assertNotEqual(old_properties, edited_jogo.to_dict())

    def test_error(self):
        jogo = mommy.save_one(Jogo)
        old_properties = jogo.to_dict()
        template_response = save(jogo.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['foto']), set(errors.keys()))
        self.assertEqual(old_properties, jogo.key.get().to_dict())
        self.assert_can_render(template_response)
