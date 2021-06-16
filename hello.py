from flask import Flask, abort, request, render_template


app = Flask(__name__) # making an instance of flask
# app.config.from_object(DevConfig)


# you should use __ name __ because depending on if it’s started as 
# application or imported as module the name will be different ('main' versus the actual import name)


# We then use the route() decorator to tell Flask what URL should trigger our function..
# The function is given a name which is also used to generate URLs for that particular function,
#  and returns the message we want to display in the user’s browser.

@app.route('/')      # In the preceding lines, we are instructing our Flask app to route all requests for / (the root URL) to this view function (index)
def hello_world():
    return 'Hello world'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/student/<name>')
def student(name):
    return render_template('user.html', name=name)
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

# if __name__ == '__hello__':
#     app.run(debug=True)


