# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from jogo_app.jogo_model import Jogo
from routes.jogos.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Jogo.query().get())
        redirect_response = save(foto='foto_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_jogo = Jogo.query().get()
        self.assertIsNotNone(saved_jogo)
        self.assertEquals('foto_string', saved_jogo.foto)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['foto']), set(errors.keys()))
        self.assert_can_render(template_response)
