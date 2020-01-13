# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.insert(0, "../")
from datastructure.Administrator import Administrator
from utils.util import load_logger

password = "mysecretpassword"
mail = "alessiosavibtc@gmail.com"
log = load_logger("debug", "test_log", "pyrecognizer.log")
a = Administrator("alessio", mail, password)
a.init_redis_connection()


class TestAdmin(unittest.TestCase):

    def test_a_connection(self):
        self.assertTrue(a.init_redis_connection())

    def test_b_invalid_password(self):
        self.assertFalse(a.validate_password("a"))
        self.assertFalse(a.validate_password("1"))
        self.assertFalse(a.validate_password("aaaa"))

    def test_c_valid_password(self):
        self.assertTrue(a.validate_password("aaaaa"))
        self.assertTrue(a.validate_password("11111"))
        self.assertTrue(a.validate_password("!!!!!"))
        self.assertTrue(a.validate_password(password))

    def test_d_register_user(self):
        self.assertTrue(a.add_user())

    def test_e_login_user(self):
        self.assertTrue(a.verify_login(password))

    def test_f_remove_user(self):
        self.assertTrue(a.remove_user())
