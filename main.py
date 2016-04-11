from flask import Flask, render_template

import requests
import pprint as pp
import json
import os

api_key = "13~ai4isuqQYZlTRv6YzBHPIAM05epVD2Fd1e9u7ypHFNjZSEH9xb0JHpWamMUFYngw"
base_url = "https://webcourses.ucf.edu"


class DataObject(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

class WebcourseObject(object):
    def __init__(self, base_url, course_id, api_key, data=None):
        self.base_url = base_url
        self.api_key = api_key
        self.course_id = course_id
        if data is None:
            self.obj = DataObject()
        else:
            self.obj = DataObject(**data)
            self._process_data(data)

    def _process_data(self, data):
        # provides a hook for explicitly handling raw object data
        pass

class Course(WebcourseObject):

    @property
    def course_modules_url(self):
        return '{base}/api/v1/courses/{cid}/modules?access_token={key}'.format(
            base=self.base_url,
            cid=self.course_id,
            key=self.api_key
        )

    @property
    def modules(self):
        if not hasattr(self, '_modules'):
            return None
        return self._modules

    def get_modules(self):
        response = requests.get(self.course_modules_url)
        response_dicts = response.json()
        self._modules = [
            Module(
                self.base_url, self.course_id, self.api_key, data=mod
            ) for mod in response_dicts
        ]
        return self._modules
    
    def __str__(self):
        return '[{0}] {1}'.format(self.id, self.name)

class Module(WebcourseObject):

    @property
    def items_url(self):
        return '{base}/api/v1/courses/{cid}/modules?access_token={key}'.format(
            base=self.base_url,
            cid=self.course_id,
            key=self.api_key
        )

    def get_items(self):
        # complete function to get items
        pass

    def __str__(self):
        return '[{0}] {1}'.format(self.id, self.name)
    

app = Flask(__name__)

@app.route("/") # uses the GET method
@app.route("/<user>")
def index(user=None):
    return render_template("user.html", user=user)

@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html", name=name)

@app.route("/class_list")
def template_test():

    url = "%s/api/v1/courses?access_token=%s" % (base_url, api_key)

    my_string = "Classes"
    return render_template('class_list.html', my_string=my_string, my_list=[0,1,2,3,4,5])


if __name__ == "__main__":
    # response = requests.get('someurl')
    # with open('filename.html', 'wb') as outfile:
    #     outfile.write(response.content)
    app.run()