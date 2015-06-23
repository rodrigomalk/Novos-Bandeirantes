# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from jogo_app.jogo_model import Jogo
from routes.jogos.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Jogo)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        jogo = mommy.save_one(Jogo)
        redirect_response = delete(jogo.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(jogo.key.get())

    def test_non_jogo_deletion(self):
        non_jogo = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_jogo.key.id())
        self.assertIsNotNone(non_jogo.key.get())

