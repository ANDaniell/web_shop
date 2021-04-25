import pytest
import unittest

from data import db_session
from data.dbworker import DBWorker

dbworker = DBWorker()


def test_user():
    dbworker.add_user('Daniel', 'email@gmail.com', 'password')
