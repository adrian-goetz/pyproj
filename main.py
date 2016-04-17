from flask import Flask, jsonify, request, render_template, url_for

import requests # may need to pip install requests
import pprint as pp
import json
import os #  Used for managing files and folders
import urllib #  Used for downloading files from URL

from data_access_objects import WebcourseObject, Course, Module, CourseItem

web_courses_obj = WebcourseObject()

app = Flask(__name__)

@app.route("/")  # uses the GET method
def index():
    return render_template("main.html", user="Adrian")

@app.route("/take_it_offline/")
def take_it_offline():
    return render_template("take_it_offline.html", wco = web_courses_obj)  # pass object information here

@app.route("/modules_list/", methods=['POST'])
def modules_list():
    course_name=request.form['course']
    
    temp_list = web_courses_obj._get_courses()

    for item in temp_list:
        if item.get_name() == course_name:
            this_course = item

    these_modules = this_course.get_modules()

    return render_template(
        'modules_list.html',
        course_obj=this_course,
        module_list=these_modules)

@app.route("/selected_items/", methods=['POST'])
def selected_items():
    #  This should return a list of the urls of all the checked boxes
    items_selected = request.form.getlist('check')
    item_data = []

    for item in items_selected:
        item_data.append(request.json(item['url']))

    #  From there you can check the type of object
    #  If type is Page, it will have the body tag
    #  If type is File, it will have the download tag
    # testfile = urllib.URLopener()
    # testfile.retrieve("http://randomsite.com/file.gz", "file.gz")

    return 1

@app.route("/youre_a_star/")
@app.route("/final_quest/")
def construction():
    return render_template("under_construction.html")



# use this to make directories
# os.makedirs('/path/to/directory')

# for creating files:
# http://code.runnable.com/UiIdhKohv5JQAAB6/how-to-download-a-file-generated-on-the-fly-in-flask-for-python

if __name__ == "__main__":
    # response = requests.get('someurl')
    # with open('filename.html', 'wb') as outfile:
    #     outfile.write(response.content)
    app.debug = True
    app.run()