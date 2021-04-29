
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
import db_session
from goods import Good


class GoodListResource(Resource):
    def get(self):
        session = db_session.create_session()
        goods = session.query(Good).all()
        return jsonify({'goods': [item.to_dict(only=(
            'name',
            'price',
            'about',
            'characteristics',
            'amount',
            'tags'
        )) for item in goods]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price',type=float ,required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('about', required=False, type=str)
        parser.add_argument('characteristics', required=False, type=str)
        parser.add_argument('discount', required=False, type=float)
        parser.add_argument('amount', required=False, type=int)

        args = parser.parse_args()
        session = db_session.create_session()
        good = Good(
            price=args['price'],
            name=args['name'],
            age=args['age'],
            about=args['about'],
            characteristics=args['characteristics'],
            discount=args['discount'],
            amount=args['amount']
        )
        session.add(good)
        session.commit()
        return jsonify({'success': 'OK'})


class GoodResource(Resource):
    def get(self, good_id):
        abort_if_good_not_found(good_id)
        session = db_session.create_session()
        good = session.query(Good).get(good_id)
        return jsonify({'good': good.to_dict(only=('name',
                            'price',
                            'about',
                            'characteristics',
                            'discount',
                            'tags'
        ))})

    def delete(self, good_id):
        abort_if_good_not_found(good_id)
        session = db_session.create_session()
        good = session.query(Good).get(good_id)
        session.delete(good)
        session.commit()
        return jsonify({'success': 'OK'})

    def patch(self, good_id):
        abort_if_good_not_found(good_id)
        session = db_session.create_session()
        good = session.query(Good).get(good_id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('price', required=False, type=float)
        parser.add_argument('about', required=False, type=str)
        parser.add_argument('characteristics', required=False, type=str)
        parser.add_argument('discount', required=False, type=float)
        parser.add_argument('amount', required=False, type=int)
        args = parser.parse_args()
        session.update(good)
        session.commit()
        return jsonify({'good': good.to_dict(only=('name',
                            'price',
                            'about',
                            'characteristics',
                            'discount',
                            'tags'
        ))})


def abort_if_good_not_found(good_id):
    session = db_session.create_session()
    good = session.query(Good).get(good_id)
    if not good:
        abort(404, message=f"Good {good_id} not found")
