from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    DB.init_app(app)

    @app.route('/')
    def root():

        users = User.query.all()

        return render_template('base.html', title='Home', users=users)

    @ app.route('/populate')
    def populate():
        add_or_update_user('ryanallred')
        add_or_update_user('nasa')
        return render_template('base.html', title='Populate')

    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)
       
        return render_template('base.html', title='Update')

    @app.route('/reset')
    def reset():

        # resetting the database
        DB.drop_all()
        DB.create_all()

        return render_template('base.html', title='Reset')
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User "{name}" was successfully added.'

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f"Error adding {name}: {e}"
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare users to themselves silly'
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = f'"{request.values[tweet_text]}" is more likely to be said by {} than {}'.format(request.values['tweet_text'],
                                                                                                       user1 if prediction else user0,
                                                                                                       user0 if prediction else user1)

    return app
