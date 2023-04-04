from flask import Flask, render_template, make_response, jsonify, redirect
from flask_login import login_user, login_required, logout_user, login_manager, LoginManager

from data import db_session
from data.albums import Album
from data.groups import Group
from data.musicians import Musician
from data.songs import Song
from data.users import User
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
# api = Api(app)
app.config['SECRET_KEY'] = 'the_freaking_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/music.db")
    # db_sess = db_session.create_session()
    # while True:
    #     band = Song()
    #     band.name = str(input())
    #     band.album_id = 2
    #     db_sess.add(band)
    #     db_sess.commit()
    # app.register_blueprint(news_api.blueprint)
    app.run(port=8000, host='127.0.0.1')


@app.route("/")
def index():
    return render_template("infopage.html")


# -------------------- списки --------------------
@app.route("/groups")
def group_list():
    db_sess = db_session.create_session()
    bands = [band for band in db_sess.query(Group).all()]
    return render_template("group_page.html", bands=bands)


@app.route("/musicians")
def author_list():
    db_sess = db_session.create_session()
    authors = [mus for mus in db_sess.query(Musician).all()]
    return render_template("musician_page.html", authors=authors)
# -------------------- списки --------------------


# -------------------- конкретные вещи --------------------
@app.route("/group/<id>")
def band_page(id):
    db_sess = db_session.create_session()
    band = db_sess.query(Group).get(id)
    albums = [al for al in db_sess.query(Album).filter(Album.group == band)]
    musicians = [mus for mus in db_sess.query(Musician).filter(Musician.group == band)]
    return render_template("single_band.html", band=band, albums=albums, musicians=musicians)


@app.route("/musician/<id>")
def author_page(id):
    db_sess = db_session.create_session()
    author = db_sess.query(Musician).get(id)
    bands = [band for band in db_sess.query(Group).filter(Group.name == author.group.name)]
    return render_template("single_musician.html", author=author, bands=bands)


@app.route("/group/<id>/album/<aid>")
def album_page(id, aid):
    db_sess = db_session.create_session()
    band = db_sess.query(Group).get(id)
    album = db_sess.query(Album).get(aid)
    songs = [track for track in db_sess.query(Song).filter(Song.album == album)]
    return render_template("single_album.html", album=album, band=band, songs=songs)
# -------------------- конкретные вещи --------------------


# -------------------- загрузка фоток --------------------
#  @app.route("/group/<id>/add_photo", methods=['POST'])
#  def band_photo(id):
#      db_sess = db_session.create_session()
#      band = db_sess.query(Group).get(id)
#      form = PicAddForm()
# -------------------- загрузка фоток --------------------


# -------------------- регистрация/авторизация --------------------
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
# -------------------- регистрация/авторизация --------------------


# -------------------- ошибки --------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(500)
def app_error(error):
    return make_response(jsonify({'error': 'App error'}), 500)
# -------------------- ошибки --------------------


if __name__ == '__main__':
    main()
