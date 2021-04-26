def clear_data():
    os.remove("db/blogs.db")


def add_item(name, price, pth_to_img_avatar, about, char, amount, tags=None, discount=None):
    db_sess = db_session.create_session()
    item = Good(
        name=str(name),
        price=float(price),
        avatar=str(pth_to_img_avatar),
        about=str(about),
        characteristics=str(char),
        amount=int(amount),
        # tags=db_sess.query(Tag).filter(Tag.id == 1).all()
    )
    if tags:
        item.tags = db_sess.query(Tag).filter(eval(tags)).all()
    if discount:
        item.discount = float(discount)

    db_sess.add(item)
    db_sess.commit()


def add_item_image(path_to_img, item_id):
    db_sess = db_session.create_session()
    item_img = item_image(
        path=str(path_to_img),
        item_id=int(item_id)
    )
    db_sess.add(item_img)
    db_sess.commit()


def add_tag_to_item(item_id, tag_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == item_id).first()
    tag = db_sess.query(Tag).filter(Tag.id == tag_id).first()
    item.tags.append(tag)
    db_sess.commit()


def add_tag(name):
    db_sess = db_session.create_session()
    tag = Tag(
        name=str(name)
    )
    db_sess.add(tag)
    db_sess.commit()


def add_order(item_id, user_id, address_id, price=0, status_id=1):
    db_sess = db_session.create_session()
    order = Order(
        total_price=float(price),
        status_id=int(status_id),
        goods_by_order = db_sess.query(Good).filter(Good.id == 2).all()
    )
    # order.goods = db_sess.query(Good).filter(Good.id == 2).all()
    order_id = order.id
    if user_id:
        order.user_id = int(user_id)
    if address_id:
        order.address_id = int(address_id)
    db_sess.add(order)
    db_sess.commit()
    add_item_to_order(item_id, order_id)


def add_item_to_order(item_id, order_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == item_id).first()
    order = db_sess.query(Order).filter(Order.id == order_id).first()
    order.goods.append(item)
    db_sess.commit()


def add_status(name):
    db_sess = db_session.create_session()
    status = Status(
        name=str(name)
    )
    db_sess.add(status)
    db_sess.commit()


def add_user(name, email, password, address_id=None, card=None):
    db_sess = db_session.create_session()
    user = User(
        name=str(name),
        email=str(email),
        hashed_password=str(password),
        hashed_card=str(card)
    )
    if address_id:
        user.address_id = int(address_id)
    if card:
        user.hashed_card = int(card)
    db_sess.add(user)
    db_sess.commit()


def add_favourite(item_id, user_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == int(item_id)).first()
    user = db_sess.query(User).filter(User.id == int(user_id)).first()
    user.favourites.append(item)
    db_sess.commit()


def add_review(grade, item_id, user_id=None, about=None):
    db_sess = db_session.create_session()
    rewiew = Review(
        grade=int(grade),

        good_id=int(item_id)
    )
    if about:
        rewiew.about = str(about)
    if user_id:
        rewiew.user_id = int(user_id)
    db_sess.add(rewiew)
    db_sess.commit()


def add_address(city, region):
    db_sess = db_session.create_session()
    address = Address(
        city=str(city),
        region=str(region)
    )
    db_sess.add(address)
    db_sess.commit()

{{url_for('static', filename='styles/style.css')}}
<img src="http://127.0.0.1:5000/img/{{img}}" alt="альтернативный текст">

<h2>{{item["head"]}}</h2>
<div>{{item["about"]}}</div>