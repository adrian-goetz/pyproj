from flask import Flask, request

app = Flask(__name__) # app is Flask Object. Name helps it determine the route path

# @ signifies a decorator - way to wrap a function and modifying its behavior
@app.route('/') # root directory / homepage of the website
def index(): # routing/mapping. Whenever a user goes to homepage, they will see the index object
	return 'This is the homepage'

# mapping url to return value of a function


@app.route('/tuna')
def tuna():
	return '<h2>Tuna is good</h2>'

# create html template and pass in variables

@app.route('/profile/<username>') # if you want a variable in the address, put it in the the brackets - basic strings
def profile(username):
	return "Hey there %s" % username


# using integers
@app.route('/post/<int:post_id>')
def show_post(post_id): # function does not have to be the same name as the address
	return '<h2>Post id is %s</h2>' % post_id



@app.route("/bacon", methods=['GET', 'POST']) # this page is capable of handling both GET and POST
def index():
	if request.method == 'POST':
		return "You are using POST"
	else:
		return "You are probably using GET"


if __name__ == '__main__': # quick check to make sure we only run the app when the file is called directly
	app.run(debug=True) # start the app. Refresh when updated

 # * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

