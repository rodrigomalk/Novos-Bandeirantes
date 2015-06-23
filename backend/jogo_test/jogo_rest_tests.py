# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from jogo_app.jogo_model import Jogo
from routes.jogos import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Jogo)
        mommy.save_one(Jogo)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        jogo_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'foto']), set(jogo_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Jogo.query().get())
        json_response = rest.new(None, foto='foto_string')
        db_jogo = Jogo.query().get()
        self.assertIsNotNone(db_jogo)
        self.assertEquals('foto_string', db_jogo.foto)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['foto']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        jogo = mommy.save_one(Jogo)
        old_properties = jogo.to_dict()
        json_response = rest.edit(None, jogo.key.id(), foto='foto_string')
        db_jogo = jogo.key.get()
        self.assertEquals('foto_string', db_jogo.foto)
        self.assertNotEqual(old_properties, db_jogo.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        jogo = mommy.save_one(Jogo)
        old_properties = jogo.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, jogo.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['foto']), set(errors.keys()))
        self.assertEqual(old_properties, jogo.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        jogo = mommy.save_one(Jogo)
        rest.delete(None, jogo.key.id())
        self.assertIsNone(jogo.key.get())

    def test_non_jogo_deletion(self):
        non_jogo = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_jogo.key.id())
        self.assertIsNotNone(non_jogo.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

