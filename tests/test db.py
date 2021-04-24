import unittest
import pytest

from data import db_session
from main import add_address, add_user, add_tag, add_item, add_tag_to_item, add_item_image, add_order, add_status, \
    add_favourite, add_review, add_item_to_order


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


def add_all():
    add_address('Moscow', "Moscow region")
    add_user('Evgen', 'evgen@gmail.com', 'password', None, None)
    add_tag('tag 01')
    add_tag('tag 02')
    add_item('item_name', 3000, 'path_toImg', 'about', 'харктеристики', 3, 1)
    add_item('item_name2', 3001, 'path_toImg', 'about', 'харктеристики', 3, 1)

    add_tag_to_item(1, 1)
    add_item_image('путь до картинки', 1)
    add_status('status 1')
    add_order(1, 1, 1, 300, 1)

    add_item_to_order(2,1)
    add_favourite(1,1)
    add_review(4,1,1,'сообщение от user1')


if __name__ == '__main__':
    # unittest.main()
    db_session.global_init("db/blogs.db")
    add_all()
