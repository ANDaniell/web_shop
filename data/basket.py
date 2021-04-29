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
        print(request.form.get('city_user'))
        if request.form.get('Encrypt') == 'Encrypt':
            # pass
            session['current_cart'] = []
            print("Encrypted")
            return redirect('/')

        elif request.form.get('Decrypt') == 'Decrypt':
            if dbworker.get_addreass_by_value(request.form.get('city_user')) is not None:
                address = dbworker.get_addreass_by_value(request.form.get('city_user'))
                print('find')
            else:
                address = dbworker.add_address(request.form.get('city_user'))
                print(address)
            # pass # do something else
            if current_user.is_authenticated:
                user = current_user.get_id()
                print('user:', user)
                print('session:', session['current_cart'])
                dbworker.add_order(111, 1, session['current_cart'], int(user), address)
                session['current_cart'] = []
            else:
                print(session['current_cart'])
                dbworker.add_order(111, 1, session['current_cart'], None, address)
                session['current_cart'] = []
            print("Decrypted")
            return redirect('/')
        elif 'Remove' in str(request.form):
            lst = request.form.get('Remove').split()
            a = int(lst[1])
            print(session['current_cart'])
            print('---'*10)
            arr = []
            for i in session['current_cart']:
                if a != i:
                    arr.append(i)
            print(session['current_cart'])
            session['current_cart'] = arr
            if session['current_cart'] == [] or session['current_cart'] is None:
                return redirect('/')
            else:
                return redirect('/basket')
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
