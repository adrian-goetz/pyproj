import requests  # may need to pip install requests
import pprint as pp
import os  # Used for managing files and folders
import logging
from zipfile import ZipFile

from flask import Flask, request, render_template

from data_access_objects import WebcourseObject, CourseItem

web_courses_obj = WebcourseObject()

app = Flask(__name__)
log = logging.getLogger(__name__)


@app.route("/")  # uses the GET method
def index():
    return render_template("main.html", user="Adrian")


@app.route("/take_it_offline/")
def take_it_offline():  # pass object information here
    return render_template("take_it_offline.html", wco=web_courses_obj)


@app.route("/modules_list/", methods=['POST'])
def modules_list():
    course_name = request.form['course']

    for item in web_courses_obj.course_list:
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
    # body html uses unicode

    form_data = [
        CourseItem.from_url(
            url
        ) for url in request.form.getlist('module_items')
    ]

    with ZipFile('course-archive.zip', 'w') as z_file:
        for obj in form_data:
            z_file.writestr(
                obj.file_path,
                obj.item_content()
            )

    # get the title and url of each object
    # attach the access code to the url
    # From there you can check the type of object
    # If type is Page, it will have the body tag
    # If type is File, it will have the download tag
    # testfile = urllib.URLopener()
    # testfile.retrieve("http://randomsite.com/file.gz", "file.gz")

    return render_template(
        'download_page.html',
        data=form_data,
        item_count=len(request.form))


@app.route("/youre_a_star/")
@app.route("/final_quest/")
def construction():
    return render_template("under_construction.html")


# use this to make directories
# os.makedirs('/path/to/directory')

# with open('filename.html', 'wb') as outfile:
#     outfile.write(response.content)

# for creating files:
# http://code.runnable.com/UiIdhKohv5JQAAB6/how-to-download-a-file-generated-on-the-fly-in-flask-for-python

if __name__ == "__main__":
    if web_courses_obj.errors:
        errmsg = '[{0}] could not access webcourses!'
        app.logging.error(errmsg.format(web_courses_obj.code))
    else:
        app.config.update(WTF_CSRF_ENABLED=False)
        app.run(debug=True)
