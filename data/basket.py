import flask
from flask import make_response, render_template, session, request
from flask_login import current_user
from werkzeug.utils import redirect

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
    try:
        goods = session['current_cart']
        data = []
        for i in goods:
            gg = dbworker.get_good(i)
            total = gg['price']
            data.append(gg)
    except Exception:
        data = None
    city = {'city': 'Город'}
    if current_user.is_authenticated:
        # print(dbworker.get_user(current_user.get_id()))
        city = dbworker.get_address_by_user(current_user.get_id())
    if request.method == 'GET':
        return make_response(render_template('basket.html', data=data, city=city))
    if request.method == 'POST':
        if request.form.get('Encrypt') == 'Encrypt':
            # pass
            session['current_cart'] = []
            print("Encrypted")
            return redirect('/')

        elif request.form.get('Decrypt') == 'Decrypt':
            # pass # do something else
            if current_user.is_authenticated:
                user = current_user.get_id()
                dbworker.add_order(111, 1, user, 1, session['current_cart'])
            else:
                print(session['current_cart'])
                dbworker.add_order(111, 1, None, 1, session['current_cart'])
                session['current_cart'] = []
            print("Decrypted")
            return redirect('/')
        elif 'Remove' in str(request.form):
            lst = request.form.get('Remove').split()
            a = int(lst[1])
            session['current_cart'].remove(a)
            if session['current_cart'] == [] or session['current_cart'] is None:
                return redirect('/')
        else:
            print('nothing')
        print(request.form)
        return make_response(render_template('basket.html', data=data, city=city))


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
