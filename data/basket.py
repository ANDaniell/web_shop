import flask
from flask import make_response, render_template, session, request
from flask_login import current_user

from data.dbworker import DBWorker

blueprint = flask.Blueprint(
    'busket_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/addtocart', methods=['POST'])
def add_good_to_cart():
    id_tov = int(request.get_json()['id_tov'])
    assert id_tov > 0
    print('Tovar:', id_tov)
    if 'current_cart' not in session or session['current_cart'] is None:
        print('Created new current_cart')
        session['current_cart'] = []

    # breakpoint()
    print('Current cart is', session['current_cart'])
    if id_tov not in session['current_cart']:
        print('adding')
        session['current_cart'] += [id_tov]

    print('New cart is', session['current_cart'])
    return str(len(session['current_cart']))

@blueprint.route('/basket', methods=['POST', 'GET'])
def get_basket():
    dbworker = DBWorker()
    if request.method == 'GET':
        goods = session['current_cart']
        dbworker = DBWorker()
        total = 0
        data = []
        for i in goods:
            gg = dbworker.get_good(i)
            total = gg['price']
            data.append(gg)
        city = {'city': 'Город'}
        if current_user.is_authenticated:
            #print(dbworker.get_user(current_user.get_id()))
            city = dbworker.get_address_by_user(current_user.get_id())

        return make_response(render_template('basket.html', data=data, city=city))
    if request.method == 'POST':
        pass


@blueprint.route("/session_test")
def session_test():
    res = str(session.items())
    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        session['cart_item']['items'].append({'id01': 1212})
        session.modified = True
    else:
        session['cart_item'] = cart_item
    return res
