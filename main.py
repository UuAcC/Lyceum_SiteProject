from flask import Flask, render_template, make_response, jsonify

app = Flask(__name__)
# api = Api(app)
app.config['SECRET_KEY'] = 'the_freaking_key'
# login_manager = LoginManager()
# login_manager.init_app(app)


def main():
    # db_session.global_init("db/blogs.db")
    # app.register_blueprint(news_api.blueprint)
    app.run(port=8000, host='127.0.0.1')


@app.route("/")
def index():
    return render_template("infopage.html")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
