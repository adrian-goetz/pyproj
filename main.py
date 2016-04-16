from flask import Flask, render_template

import requests # may need to pip install requests
import pprint as pp
import json
import os

from data_access_objects import WebcourseObject

web_courses_obj = WebcourseObject()

app = Flask(__name__)

@app.route("/")  # uses the GET method
def index():
    return render_template("main.html", user="Adrian")

@app.route("/youre_a_star/")
@app.route("/final_quest/")
def construction():
	return render_template("under_construction.html")

@app.route("/take_it_offline/")
def take_it_offline():
    return render_template("take_it_offline.html", wco = web_courses_obj)  # pass object information here

@app.route("/class_list")
def template_test():

    url = "%s/api/v1/courses?access_token=%s" % (base_url, api_key)

    my_string = "Classes"
    return render_template('class_list.html', my_string=my_string, my_list=[0,1,2,3,4,5])

if __name__ == "__main__":
    # response = requests.get('someurl')
    # with open('filename.html', 'wb') as outfile:
    #     outfile.write(response.content)
    app.debug = True
    app.run()