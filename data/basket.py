import flask
from flask import make_response, render_template, session

blueprint = flask.Blueprint(
    'busket_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/basket',  methods=['POST', 'GET'])
def get_basket():
    orders_sess = session.get('orders_sess', 0)
    return make_response(render_template('basket.html', data = 1))


@blueprint.route("/session_test")
def session_test():
    res = str(session.items())

    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        session['cart_item']['items'].append({'id01':1212})
        session.modified = True
    else:
        session['cart_item'] = cart_item
    return res

    '''
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    session.modified = True
    return make_response(
        f"Вы пришли на эту страницу {visits_count} раз")
    '''