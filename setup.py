from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CaloriesInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    bio = db.Column(db.String(15))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    activity = db.Column(db.String(40))

    def __init__(self, age, bio, weight, height, activity):
        self.age = age
        self.bio = bio
        self.weight = weight
        self.height = height
        self.activity = activity

    def __repr__(self):
        return '<CaloriesInfo %r' % self.id


activity_lst = ['Низкий', "Умеренный", "Высокий", "Очень высокий"]
ranges = [[x for x in range(10, 19)],
          [x for x in range(18, 30)],
          [x for x in range(30, 60)],
          [x for x in range(60, 151)]]

bio_lst = ['Мужчина', 'Женщина']


def calculate_calories(age, bio, weight, height, activity):

    def activity_validate(activity, res):
        if activity == activity_lst[0]:
            return round(res + 338, 2)
        elif activity == activity_lst[1]:
            return round(res + 481, 2)
        elif activity == activity_lst[2]:
            return round(res + 632, 2)
        elif activity == activity_lst[3]:
            return round(res + 853, 2)

    if age in ranges[0] and bio == bio_lst[0]:
        res = 16.6 * weight + 119 * (height / 100) + 572
        return activity_validate(res, activity)

    if age in ranges[0] and bio == bio_lst[1]:
        res = 7.4 * weight + 482 * (height / 100) + 217
        return activity_validate(activity, res)

    if age in ranges[1] and bio == bio_lst[0]:
        res = 15.4 * weight + 27 * (height / 100) + 717
        return activity_validate(activity, res)

    if age in ranges[1] and bio == bio_lst[1]:
        res = 13.3 * weight + 334 * (height / 100) + 35
        return activity_validate(activity, res)

    if age in ranges[2] and bio == bio_lst[0]:
        res = 11.3 * weight + 16 * (height / 100) + 901
        return activity_validate(activity, res)

    if age in ranges[2] and bio == bio_lst[1]:
        res = 8.7 * weight + 25 * (height / 100) + 865
        return activity_validate(activity, res)

    if age in ranges[3] and bio == bio_lst[0]:
        res = 8.8 * weight + 1182 * (height / 100) - 1071
        return activity_validate(activity, res)

    if age in ranges[3] and bio == bio_lst[1]:
        res = 9.2 * weight + 637 * (height / 100) - 302
        return activity_validate(activity, res)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        age = request.form['age']
        bio = request.form['bio']
        weight = request.form['weight']
        height = request.form['height']
        activity = request.form['activity']
        res = calculate_calories(int(age), bio, float(weight), float(height), activity)
        info = CaloriesInfo(age, bio, weight, height, activity)

        try:
            db.session.add(info)
            db.session.commit()
            return render_template('main/result.html', res=res)
        except:
            return 'Error'

    else:
        return render_template('main/home.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)