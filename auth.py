from datetime import datetime
from flask import  render_template, request, flash, redirect, url_for
from models import User, Les, Rooster
from __init__ import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/', endpoint='home')
@login_required
def home():
    our_users = User.query.order_by(User.email)
    return render_template('index.html',
    our_users=our_users)


@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    user_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.role = request.form['verander_role']
        try:
            db.session.commit()
            flash("update gelukt!")
            return redirect(url_for('admin'))
        except:

            return "er was een probleem"
    else:
        return render_template("update.html", user_to_update=user_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('user deleted succesfully!')
        return redirect(url_for('admin'))

    except:
        return 'er was een probleem'

@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
             flash('Email already exists.', category='error')
        if len(email) < 4:
            flash("Email is too short!", category='error')
        elif len(password) < 7:
            flash("password too short!", category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password, method="sha256"))
            # new_user.role = "admin"
            if current_user.is_authenticated == True:
                if current_user.role == "admin":
                    new_user.role = "instructeur"
                    db.session.add(new_user)
                    db.session.commit()
            else:
                new_user.role = "klant"
                db.session.add(new_user)
                db.session.commit()
            # login_user(user, remember=True)
            flash("Account created!", category='succes')
            return redirect(url_for("login"))


    return render_template("signup.html")

@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in succesfully!")
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash("incorrect password, try again.")
        else:
            flash("Email does not exist.")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succesfully logged out!")
    return redirect(url_for('login'))

@app.route('/updateles', methods=["POST", "GET"])
def create_les():
    if request.method == "POST":
        les = request.form['les']
        datum_str = request.form['datum']



        datum = datetime.strptime(datum_str, '%Y-%m-%dT%H:%M')


        new_les = Les(les=les, datum=datum)
        try:
            db.session.add(new_les)
            db.session.commit()
            return redirect(url_for('les'))
        except:
            return "er ging iets mis"
    return render_template("updateles.html")





@app.route('/lessen.html', endpoint='les', methods=["POST", "GET"])
@login_required
def les():
    lessen = Les.query.order_by(Les.id)
    return render_template('lessen.html', lessen=lessen)





@app.route('/lessen.html/<int:id>', methods=["POST", "GET"])
def schrijfin(id):

    if request.method == "POST":
        les = Les.query.get_or_404(id)
        nieuwe_les = Rooster(email=current_user.email, les_id=les.id)
        try:
            db.session.add(nieuwe_les)
            db.session.commit()
            flash("ingeschreven!")

        except:
            return "niet gelukt."

    return redirect(url_for('les'))


@app.route('/instructeur.html', endpoint='instructeur')
def instructeur():
    role = current_user.role
    users = Rooster.query.order_by(Rooster.les_id)
    our_users = User.query.order_by(User.email)
    if role == "instructeur" or role == "admin":
        return render_template('instructeur.html', our_users=our_users, users=users )
    else:
        flash("you do not have permission!")
        return redirect(url_for('home'))


@app.route('/admin.html', endpoint='admin')
def admin():
    role = current_user.role
    users = Rooster.query.order_by(Rooster.les_id)
    our_users = User.query.order_by(User.email)
    if role == "admin":
        return render_template('admin.html',
        our_users=our_users, users=users )
    else:
        flash("you do not have permission!")
        return redirect(url_for('home'))



if __name__ == '__main__':
    app.run()