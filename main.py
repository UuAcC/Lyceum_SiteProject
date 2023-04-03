from flask import Flask, render_template, make_response, jsonify
from data import db_session
from data.albums import Album
from data.groups import Group
from data.musicians import Musician
from data.songs import Song

app = Flask(__name__)
# api = Api(app)
app.config['SECRET_KEY'] = 'the_freaking_key'
# login_manager = LoginManager()
# login_manager.init_app(app)


def main():
    db_session.global_init("db/music.db")
    # db_sess = db_session.create_session()
    # band = Song()
    # band.name = str(input())
    # band.group_id = int(input())
    # db_sess.add(band)
    # db_sess.commit()
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
    return render_template("musician_page.html", authors=authors, db=db_sess, Group=Group)
# -------------------- списки --------------------


# -------------------- конкретные вещи --------------------
@app.route("/group/<id>")
def band_page(id):
    db_sess = db_session.create_session()
    band = db_sess.query(Group).get(id)
    albums = [al for al in db_sess.query(Album).filter(Album.group_id == band.id)]
    musicians = [mus for mus in db_sess.query(Musician).filter(Musician.group_id == band.id)]
    return render_template("single_band.html", band=band, albums=albums, musicians=musicians)


@app.route("/musician/<id>")
def author_page(id):
    db_sess = db_session.create_session()
    author = db_sess.query(Musician).get(id)
    bands = [band for band in db_sess.query(Group).filter(Group.id == author.group_id)]
    return render_template("single_musician.html", author=author, bands=bands)


@app.route("/group/<id>/album/<aid>")
def album_page(id, aid):
    db_sess = db_session.create_session()
    band = db_sess.query(Group).get(id)
    album = db_sess.query(Album).get(aid)
    songs = [track for track in db_sess.query(Song).filter(Song.album_id == aid)]
    return render_template("single_album.html", album=album, band=band, songs=songs)
# -------------------- конкретные вещи --------------------


# -------------------- ошибки --------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)
# -------------------- ошибки --------------------


if __name__ == '__main__':
    main()
