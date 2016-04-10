import requests
import pprint as pp
import json
import os

api_key = "13~ai4isuqQYZlTRv6YzBHPIAM05epVD2Fd1e9u7ypHFNjZSEH9xb0JHpWamMUFYngw"
base_url = "https://webcourses.ucf.edu"
course_id = "1166450"

# url = "%s/api/v1/courses/%s?access_token=%s" % (base_url, course_id, api_key)
url = "%s/api/v1/courses?access_token=%s" % (base_url, api_key)
response = requests.get(url)

course_dicts = response.json() # array of dicts

DataObject(1, 2, 3, 4, 5, blue=5, red=4) # 1-5 are *args, blue and red are **kwargs

class DataObject(object):
    def __init__(self, *args, **kwargs):
        # *args takes arguments but does not include anything passed as a keyword argument
        # **kwargs incorporates the keywords and arguments in a dictionary
        for key in kwargs:
            setattr(self, key, kwargs[key])

class WebcourseObject(object):
    def __init__(self, base_url, course_id, api_key, data=None):
        self.base_url = base_url
        self.api_key = api_key
        self.course_id = course_id

        self.obl = DataObject(**data) # ** tells it to expand data dictionary into keyword argumnts

        if data is not None:
            self._process_data(data)
        self.data = data

    def _process_data(self, data):
        pass

class Module(WebcourseObject):
    def _process_data(self, data):
        # do stuff
        pass

class Course(object):
    def __init__(self, base_url, course_id, api_key, data=None):
        self.base_url = base_url
        self.course_id = course_id
        self.base_url = base_url
        self.api_key = api_key
        self.data = data
        self.modules = None

    @property
    def course_modules_url(self):
        return "{base}/api/v1/courses/{cid}/modules?access_token={key}".format(
            base = self.base_url, 
            cid = self.course_id, 
            key = self.api_key)

    def get_modules(self):
        if self.modules is not None:
            return self.modules
        response = requests.get(self.course_modules_url)
        response_dicts = response.json()
        self.modules = [
            Module(
                base_url=self.base_url, course_id=self.course_id, api_key=self.api_key, data=mod 
            ) for mod in response_dicts
        ]
        return self.modules
    

class Module(object):
    def __init__(self, base_url, course_id, api_key, data=None):
        self.base_url = base_url
        self.course_id = course_id
        self.api_key = api_key
        self.data = data
        if data is not None:
            self.module_id = data['id']
            self.name = data['name']

    def get_items(self):
        pass

    def __str__(self):
        return '[{0}] {1}'.format(self.module_id, self.name)


class ModuleItem(object):
    def __init__(self, base_url, course_id, module_id, api_key, data=None):
        self.base_url = base_url
        self.course_id = course_id
        self.module_id = module_id
        self.api_key = api_key
        if data is not None:
            self.item_id = data['id']
            self.name = data['name']


courses = []

for cour in course_dicts:
    courses.append(Course(base_url=base_url, course_id=cour['id'], api_key=api_key, data=cour))

for item in courses:
    for m in item.get_modules():
        print m
        pp.pprint(m.data)
# PEP 8 code layout and style guidelines

# Place the file somewhere
# 
# response = requests.get(some_url)
# with open('filename.html', 'wb') as outfile:
#     outfile.write(response.content)