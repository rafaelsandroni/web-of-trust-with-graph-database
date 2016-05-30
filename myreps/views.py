from .models import User, get_todays_recent_posts
from flask import Flask, request, session, redirect, url_for, render_template, flash, Response, jsonify, json
from json import dumps

app = Flask(__name__)

@app.route('/')
def index():
    posts = 'teste'
    #get_todays_recent_posts()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('A user with that username already exists.')
        else:
            session['username'] = username

            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if not title:
        flash('You must give your post a title.')
    elif not tags:
        flash('You must give your post at least one tag.')
    elif not text:
        flash('You must give your post a text body.')
    else:
        User(session['username']).add_post(title, tags, text)

    return redirect(url_for('index'))

@app.route('/add_review', methods=['POST'])
def add_review():

    rating = request.form['rating']
    text = request.form['text']
    other = request.form['user_review']

    if not rating:
        flash('You must give your review rating.')
    elif not text:
        flash('You must give your post at least one word.')
    elif not other:
        flash('Nao ha usuario...')
    else:
        User(session.get('username')).add_review(other, rating, text)

    return profile(other)



@app.route('/like_post/<post_id>')
def like_post(post_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to like a post.')
        return redirect(url_for('login'))

    User(username).like_post(post_id)

    flash('Liked post.')
    return redirect(request.referrer)

@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    posts = user_being_viewed.get_recent_posts()

    similar = []
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
            reviews = logged_in_user.get_reviews_from(logged_in_user.username)
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)
            reviews = logged_in_user.get_reviews_from(user_being_viewed.username)


    return render_template(
        'new_profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common,
        reviews=reviews,
    )


@app.route("/search", methods=['POST','GET'])
def get_search():
    try:
        q = request.form['txt_search']
        #args["q"]
    except KeyError:
        return []
    else:
        results = User(session.get('username')).search(q)

        return render_template(
            'discover.html',
            results=results,
        )
@app.route('/discover')
def discover():
    return render_template('discover.html', tags='#nome')

@app.route('/new_profile')
def new_profile():
    return render_template('new_profile.html', app='profile')




@app.route("/get_listing")
def get_listing():

    return jsonify({'name':'Rafael Sandroni','user':'rafaelsandroni','picture':'https://getmdl.io/templates/dashboard/images/user.jpg','reviews':'22','score':'TOP'})


#OAuth

from flask_oauth import OAuth

oauth = OAuth()

FACEBOOK_APP_ID = '1562276827406360'
FACEBOOK_APP_SECRET = '005e8d19cb24bfb35c5dea8c71968e7d'

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,user_photos'}
)


@app.route('/registerWithFacebook')
def registerWithFacebook():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,action='register',
        _external=True))

@app.route('/loginWithFacebook')
def loginWithFacebook():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,action='login',
        _external=True))

@app.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['oauth_token'] = (resp['access_token'], '')
    #me = facebook.get('/me')

    me = facebook.get('/me?fields=id,name,first_name,last_name,age_range,link,gender,locale,timezone,updated_time,verified,friends,email,picture')

    about = me.data
    username = me.data['email']
    password = me.data['id']

    if request.args.get('action') == 'register':
        if User(username).registerWithFacebook(about):
            session['username'] = username
            session['name'] = about['name']
            if not about['picture']['data']['url'] :
                session['user_picture'] = "https://getmdl.io/templates/dashboard/images/user.jpg"
            else:
                session['user_picture'] = about['picture']['data']['url']


            flash('Logged in.')
            return redirect(url_for('index'))
        else:
            flash("Invalid Register")

    else:
            if User(username).verify_password(password):
                session['username'] = username
                flash('Logged in.')
                return redirect(url_for('index'))
            else:
                flash('Invalid login.')

    return redirect( request.args.get('next') )

    #return "Logged in as %s<br>%s<br>%s<br>%s<br>%s<br>%s<br>%s<br>%s<br>" % tuple(me.data)
    #return 'Logged in as id=%s email%s name=%s me=%s redirect=%s' % \
    #    (me.data['id'], me.data['email'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
