import logging
from zipfile import ZipFile

from flask import Flask, request, render_template

from data_access_objects import WebcourseObject, CourseItem

web_courses_obj = WebcourseObject()

app = Flask(__name__)
log = logging.getLogger(__name__)


@app.route("/")  # uses the GET method
def index():
    """
    Replaces index.html location.
    Provides links to take_it_offline, final_quest, and youre_a_star
    Locations final_quest and youre_a_star not yet developed.
    """
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

    return render_template(
        'download_page.html',
        data=form_data,
        item_count=len(form_data))


@app.route("/youre_a_star/")
@app.route("/final_quest/")
def construction():
    return render_template("under_construction.html")


if __name__ == "__main__":
    if web_courses_obj.errors:
        errmsg = '[{0}] could not access webcourses!'
        app.logging.error(errmsg.format(web_courses_obj.code))
    else:
        app.config.update(WTF_CSRF_ENABLED=False)
        app.run(debug=True)
