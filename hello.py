import os 

from flask import Flask, abort, request, render_template, make_response, flash, url_for, session, redirect
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message



app = Flask(__name__) # making an instance of flask
app.config['SECRET_KEY'] = 'hard to guess string'   # encpription for the flask-wtf to protect all forms against cross-site request forgery (CSRF) attacks.

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')  # Configuring URL of the application database as  the key SQLALCHEMY_DATABASE_URI in the Flask configuration object.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # setting key SQLALCHEMY_TRACK_MODIFICATIONS to False to use less memory unless signals for object changes are needed
db = SQLAlchemy(app)    # db object instantiated from the class SQLAlchemy represents the database and provides access to all the functionality of Flask-SQLAlchemy

bootstrap = Bootstrap(app)  # the extensionn is initialised by passing the app as an argument
migrate   = Migrate(app, db)
mail = Mail(app)
# you should use __ name __ because depending on if it’s started as 
# application or imported as module the name will be different ('main' versus the actual import name)

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'



@app.shell_context_processor  # configuring the flask shell command  to automatically import these objects.
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


class NameForm(FlaskForm):
    name = StringField('What Is your name?',  validators=[DataRequired()])
    submit = SubmitField('Submit')

# We then use the route() decorator to tell Flask what URL should trigger our function..
# The function is given a name which is also used to generate URLs for that particular function,
#  and returns the message we want to display in the user’s browser.
@app.route('/',  methods=['GET', 'POST'])      # In the preceding lines, we are instructing our Flask app to route all requests for / (the root URL) to this view function (index)
def hello_world():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        flash('You have inputed your name!')
        return redirect(url_for('hello_world'))
        
 
        #name = form.name.data
        #form.name.data = ''   # the form field is cleared by setting that data attribute to an empty string, so that the field is blanked when the form is rendered to the page again
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/student/<name>',)
def student(name):
    return render_template('user.html', name=name)



@app.route('/makeresponse')
# The following example creates a response object and then sets a cookie in it:
def  makeresponse():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


# @app.route('/hello/<name>')
# def  hello(name):
#     return  'Hello, %s' % name

# @app.route('/hi/<firstname>')
# @app.route('/hi/')
# def hi(firstname=None):
#     if firstname is None:
#         # If no name is specified in the URL, attempt to retrieve it
#         # from the query string.
#         firstname = request.args.get('firstname')
#         if firstname:
#             return 'Hello, %s' % firstname
#     else:
#         # No name was specified in the URL or the query string.
#         abort(404)
# In addition to the URL, values can be passed to your app in the query string. The 
# query string is made up of arbitrary keys and values that are tacked onto the URL, 
# using a question-mark:
# eg /hello/?name=Charlie

# if __name__ == '__main__':
#     app.run(debug=True)



# StringField class represents HTML <input> element with a type="text" attribute.
# The first argument to the field constructors is the label that will be used when rendering the form to HTML
# The optional validators argument included in the StringField constructor defines
# a list of checkers that will be applied to the data submitted by the user before it is
# accepted. The DataRequired() validator ensures that the field is not submitted
# empty


#-------------Databases--------#

class Role(db.Model):
    __tablename__ = 'roles'
    id     =  db.Column (db.Integer, primary_key=True)
    name   =  db.Column (db.String(64), unique = True)
    users  = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(64), unique=True, index=True)
    role_id   = db.Column(db.Integer, db.ForeignKey
    ('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# -------  Database Use in functions ------#
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None ():
            user = User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

        return render_template('index.html',form=form, name=session.get('name'),known=session.get('known', False))

In this modified version of the application, each time a name is submitted the appli‐
cation checks for it in the database using the filter_by() query filter. A known vari‐
able is written to the user session so that after the redirect the information can be sent
to the template, where it is used to customize the greeting. Note that for the applica‐
tion to work, the database tables must be created in a Python shell as shown earlier.

<div class="page-header">
 <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
 {% if not known %}
Database Use in View Functions | 71 <p>Pleased to meet you!</p>
 {% else %}
 <p>Happy to see you again!</p>
 {% endif %}
</div>


'''

#------- Flask-Mail conguration for Gmail-------
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)