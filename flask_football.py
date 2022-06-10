from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class History(UserMixin, db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), nullable=False)
    League = db.Column(db.String(30), nullable=False)
    Season = db.Column(db.String(30), nullable=False)
    Date = db.Column(db.String(100), nullable=False)

class User(UserMixin, db.Model):
    # __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class standings(db.Model):
   id = db.Column('id', db.Integer, primary_key=True, unique=False )
   Team_Position = db.Column(db.Integer)
   Name = db.Column(db.String(100))
   Points = db.Column(db.Integer)
   Games_Played = db.Column(db.Integer)
   Win = db.Column(db.Integer)
   Draw = db.Column(db.Integer)
   Lose = db.Column(db.Integer)
   Goals_Scored = db.Column(db.Integer)
   Goals_Concerned = db.Column(db.Integer)
   League = db.Column(db.String(100))
   Season = db.Column(db.Integer)

   def __str__(self):
       return f'{self.id};{self.Name};{self.Points};{self.Games_Played};{self.Win};{self.Draw};{self.Lose};{self.Goals_Scored};{self.Goals_Concerned}'

# db.create_all()

#
# import requests
# import json
# import sqlite3
# #
#
# url = "https://api-football-v1.p.rapidapi.com/v3/standings"
#
# querystring = {"season":"2021", "league":"78"}
#
# headers = {
# 	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
# 	"X-RapidAPI-Key": "68cd65fa40mshd0152fc63f9e5fep151d51jsn9ca3f6ffeb04"}
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
#
# result_json = response.text
# res = json.loads(result_json)
# res_structured = json.dumps(res, indent=4)
# # print(res_structured)
# res = response.json()
# #2
# with open('standings.json', 'w') as file:
# 	json.dump(res, file, indent=4)
# #
# #
# #
# with open('standings.json') as file:
# 	res_dictionary = json.load(file)
# #
# laliga = res_dictionary['response'][0]['league']['standings'][0]
#
#
# # ცხრილში მოცემული იქნება ლალიგის 2021 წლის ცხრილი გუნდის დასახელება, ჩატარებული მატჩები, მოგება წაგება და ა.შ გუნდები დალაგებული იქნება პოზიციის მიხედვით ცხრილში 2021 წელს
# list_team_id = []
# list_team_names = []
# list_team_points = []
# list_team_played = []
# list_team_win = []
# list_team_draw = []
# list_team_lose = []
# list_team_goals_scored = []
# list_team_goals_concerned = []
#
#
#
# for each in laliga:
# 	list_team_id.append(each['rank'])
# 	list_team_names.append(each['team']['name'])
# 	list_team_points.append(each['points'])
# 	list_team_played.append(each['all']['played'])
# 	list_team_win.append(each['all']['win'])
# 	list_team_draw.append(each['all']['draw'])
# 	list_team_lose.append(each['all']['lose'])
# 	list_team_goals_scored.append(each['all']['goals']['for'])
# 	list_team_goals_concerned.append(each['all']['goals']['against'])
#
#
#
#
#
# for i in range(len(list_team_names)):
#     db.session.add(standings(Team_Position=list_team_id[i], Name=list_team_names[i], Points=list_team_points[i],Games_Played=list_team_played[i],
#                              Win=list_team_win[i], Draw=list_team_draw[i], Lose=list_team_lose[i], Goals_Scored=list_team_goals_scored[i],
#                              Goals_Concerned=list_team_goals_concerned[i], League='Bundesliga', Season=2021))
    # db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        else:
            session['username'] = username
        login_user(user, remember=True)
        return redirect(url_for('profile'))
        # return render_template('profile.html')
    else:
        if not current_user.is_authenticated:
            return render_template('login.html')
        else:
            return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        elif first_name == '' or last_name == '' or password == '':
            flash("Fill in all blanks!")
            return redirect(url_for('signup'))
        else:
            new_user = User(username=username, first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/table', methods=['GET', 'POST'])
def table():

    if request.form.get('League') != 'random' and request.form.get('Season') != 'random1':
        info = standings.query.filter_by(Season=request.form.get('Season'), League=request.form.get('League')).all()
        user_season = request.form.get('Season')
        user_league = request.form.get('League')
        h_league = request.form.get('League')
        h_season = request.form.get('Season')
        new_history_item = History(Username=session['username'], League=h_league, Season=h_season, Date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        db.session.add(new_history_item)
        db.session.commit()
        return render_template('table.html', info=info, season=user_season, league=user_league)
    else:
        flash('Choose League And Season!!')
        return redirect(url_for('profile'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    current_history = History.query.filter_by(Username=session['username']).all()
    return render_template('history.html', current_history=current_history)

@app.route('/leagues')
def leagues():
    return render_template('leagues.html')


if __name__=='__main__':
    app.run(debug=True)






