import flask
from flask import make_response, render_template, session

from data.dbworker import DBWorker

blueprint = flask.Blueprint(
    'busket_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/basket', methods=['POST', 'GET'])
def get_basket():
    '''
    # breakpoint()
    orders_sess = session.get('current_cart', 0)
    # orders_session = session.get('orders_sess', 0)
    # print(str(session.items()))
    print(orders_sess)'''
    goods = [1,2,3,5]
    dbworker = DBWorker()
    data = []
    for i in goods:
        data.append(dbworker.get_good(i))
    return make_response(render_template('basket.html', data=data))


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

    '''
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    session.modified = True
    return make_response(
        f"Вы пришли на эту страницу {visits_count} раз")
    '''
