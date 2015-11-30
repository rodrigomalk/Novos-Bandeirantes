# coding: utf-8

import gae
from gaepermission.model import MainUser
from models  import Result, Game
from  datetime import date

class ResultTests(gae.GAETestCase):

    def setUp(self):
        super(ResultTests, self).setUp()
        self.user = MainUser(name='vovo', email='vovo@gmail.com')
        self.user.put()
        self.game = Game(tit='teste', map='brasil')
        self.game.put()

    def test_create_new_result(self):

        result = Result.change_result_attrs(points=1, won_medal=True,
                                            game_title=self.game.tit, game=self.game,
                                            user_key=self.user.key,  duration=0.20)
        result.put()

        self.assertEquals(result.last_points, 1)
        self.assertEquals(result.game_title, self.game.tit)
        self.assertEquals(result.won_medal, True)
        self.assertEquals(result.game, self.game.key)
        self.assertEquals(result.last_duration, 0.20)
        self.assertEquals(result.best_duration, 0.20)

    def test_update_result(self):
        result = Result.change_result_attrs(points=1, won_medal=True,
                                   game_title=self.game.tit, game=self.game,
                                   user_key=self.user.key,  duration=0.20)
        result.put()

        self.assertEquals(result.best_points, 1)
        self.assertEquals(result.best_duration, 0.20)
        self.assertEquals(result.best_date, date.today())
        self.assertEquals(result.frequency, 1)

        result = Result.change_result_attrs(points=2, duration=0.10, won_medal=True,
                                            game_title=self.game.tit, game=self.game,
                                            user_key=self.user.key)

        self.assertEquals(result.best_points, 2)
        self.assertEquals(result.best_duration, 0.10)
        self.assertEquals(result.best_date, date.today())
        self.assertEquals(result.frequency, 2)
