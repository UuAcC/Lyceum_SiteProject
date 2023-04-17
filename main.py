import os

from flask import Flask, render_template, make_response, jsonify, redirect
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from flask_restful import Api
from werkzeug.utils import secure_filename

import data.api_data
from data import db_session
from data.albums import Album
from data.groups import Group
from data.musicians import Musician
from data.songs import Song
from data.users import User
from forms.add_album import AlbumAddForm
from forms.add_band import BandAddForm
from forms.add_musician import MusicianAddForm
from forms.add_picture import PicAddForm
from forms.add_tracks import SongsForm
from forms.login import LoginForm
from forms.num_of_songs import NumForm
from forms.register import RegisterForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'the_freaking_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/music.db")
    api.add_resource(data.api_data.BandsListResource, '/api/bands')
    api.add_resource(data.api_data.BandsResource, '/api/bands/<int:bands_id>')
    api.add_resource(data.api_data.MusiciansListResource, '/api/musicians')
    api.add_resource(data.api_data.MusiciansResource, '/api/musicians/<int:mus_id>')
    api.add_resource(data.api_data.UsersListResource, '/api/users')
    api.add_resource(data.api_data.UsersResource, '/api/users/<int:user_id>')
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
def tutor_list():
    db_sess = db_session.create_session()
    authors = [mus for mus in db_sess.query(Musician).all()]
    return render_template("musician_page.html", authors=authors)


@app.route("/tutorials")
def author_list():
    db_sess = db_session.create_session()
    authors = [song for song in db_sess.query(Song).filter(Song.tutor != 'None')]
    return render_template("tutorials.html", songs=authors)
# -------------------- списки --------------------


# -------------------- конкретные вещи --------------------
@app.route("/group/<int:id>")
@app.route("/group/<int:id>/<add_smth>", methods=['GET', 'POST'])
def band_page(id, add_smth=False):
    db_sess = db_session.create_session()
    band = db_sess.query(Group).get(id)
    albums = [al for al in db_sess.query(Album).filter(Album.group == band)]
    musicians = [mus for mus in db_sess.query(Musician).filter(Musician.group == band)]
    if add_smth == 'add_photo' and current_user.is_authenticated:
        form = PicAddForm()
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(f'./static/img/{band.id}_pic.jpg'))
        return render_template("single_band.html", band=band, albums=albums, musicians=musicians, form=form)
    elif add_smth == 'add_album' and current_user.is_authenticated:
        album_form = AlbumAddForm()
        if album_form.validate_on_submit():
            session = db_session.create_session()
            album = Album(
                name=album_form.name.data,
                created_date=album_form.created_date.data,
                group_id=id,
            )
            session.add(album)
            session.commit()
            return redirect(f'/group/{id}/album/{album[0].id}')
        return render_template("single_band.html", band=band, albums=albums, musicians=musicians, album_form=album_form)
    return render_template("single_band.html", band=band, albums=albums, musicians=musicians)


@app.route("/musician/<int:id>")
@app.route("/musician/<int:id>/<add_photo>", methods=['GET', 'POST'])
def author_page(id, add_photo=False):
    db_sess = db_session.create_session()
    author = db_sess.query(Musician).get(id)
    bands = [band for band in db_sess.query(Group).filter(Group.name == author.group.name)]
    if add_photo and current_user.is_authenticated:
        form = PicAddForm()
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(f'./static/img/{author.id}_auth.jpg'))
        return render_template("single_musician.html", author=author, bands=bands, form=form)
    return render_template("single_musician.html", author=author, bands=bands)


@app.route("/group/<int:id>/album/<int:aid>")
@app.route("/group/<int:id>/album/<int:aid>/<add_smth>", methods=['GET', 'POST'])
@app.route("/group/<int:id>/album/<int:aid>/<add_smth>/<int:count>", methods=['GET', 'POST'])
def album_page(id, aid, add_smth=False, count=None):
    db_sess = db_session.create_session()
    band = db_sess.query(Group).get(id)
    album = db_sess.query(Album).get(aid)
    songs = [track for track in db_sess.query(Song).filter(Song.album == album)]
    if add_smth == 'num_songs' and current_user.is_authenticated:
        numform = NumForm()
        if numform.validate_on_submit():
            return redirect(f"/group/{id}/album/{aid}/add_songs/{numform.num.data}")
        return render_template("single_album.html", album=album, band=band, songs=songs, numform=numform)
    if add_smth == 'add_songs' and current_user.is_authenticated:
        songs_form = SongsForm()
        if count >= 1:
            if songs_form.songs.__len__() == 0:
                for i in range(count):
                    songs_form.songs.append_entry()
            if songs_form.validate_on_submit():
                for s in songs_form.songs:
                    try:
                        file = s.file.data
                        file.save(os.path.join(f'./static/audio/{s.name.data}.mp3'))
                    except Exception:
                        pass
                    song = Song(
                        name=s.form.name.data,
                        album_id=aid,
                    )
                    db_sess.add(song)
                db_sess.commit()
                return redirect(f"/group/{id}/album/{aid}")
        return render_template("single_album.html", album=album, band=band, songs=songs, songs_form=songs_form)
    if add_smth == 'add_photo' and current_user.is_authenticated:
        form = PicAddForm()
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(f'./static/img/{album.id}_alb.jpg'))
        return render_template("single_album.html", album=album, band=band, songs=songs, form=form)
    return render_template("single_album.html", album=album, band=band, songs=songs)
# -------------------- конкретные вещи --------------------


# -------------------- функционал админа --------------------
@app.route('/add_band', methods=['GET', 'POST'])
def add_band():
    form = BandAddForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        band = Group(
            name=form.name.data,
            genre=form.genre.data,
            created_date=form.created_date.data,
            closed_date=form.closed_date.data,
            short_bio=form.short_bio.data,

        )
        session.add(band)
        session.commit()
        return redirect("/groups")
    return render_template('add_band.html', form=form)


@app.route('/add_musician', methods=['GET', 'POST'])
def add_musician():
    form = MusicianAddForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        mus = Musician(
            name=form.name.data,
            surname=form.surname.data,
            birth_date=form.birth_date.data,
            death_date=form.death_date.data,
            group_id=form.group_id.data,
            short_bio=form.short_bio.data,
        )
        session.add(mus)
        session.commit()
        return redirect("/musicians")
    return render_template('add_musician.html', form=form)
# -------------------- функционал админа --------------------


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
