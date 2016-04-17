import requests

import pprint
pp = pprint.PrettyPrinter(indent=4)

api_key = "13~ai4isuqQYZlTRv6YzBHPIAM05epVD2Fd1e9u7ypHFNjZSEH9xb0JHpWamMUFYngw"
access_token = "?access_token=%s" % (api_key)
web_url = "https://webcourses.ucf.edu/"
base_url = "%sapi/v1/" % (web_url)


class DataObject(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])


class WebcourseObject(object):
    def __init__(self):
        # return array of Course objects
        self.course_list = get_courses()

    def _get_courses(self):
        return self.course_list


def get_courses():
    course_list = []
    url = "%scourses/%s" % (base_url, access_token)
    response = requests.get(url)  # look into prepared response?
    for item in response.json():  # response.json() is a list of json objects
        this_course = Course(
            name=item['name'],
            id=item['id'])
        course_list.append(this_course)

    return course_list


class Course(DataObject):
    # A course has a name, id, and list of modules
    @property
    def modules(self):
        if not hasattr(self, '_modules'):
            return None
        return self._modules

    def get_modules(self):
        self._modules = get_modules(self.id)
        return self._modules

    def get_name(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "[{0}] {1}".format(self.id, self.name)

    def __repr__(self):
        return "[{0}] {1}".format(self.id, self.name)


# returns modules in a course based on course_id
def get_modules(cid):
    module_list = []
    url = "%scourses/%s/modules%s" % (base_url, cid, access_token)
    response = requests.get(url)
    for item in response.json():
        this_module = Module(
            name=item['name'],
            mid=item['id'],
            items_url=item['items_url'],
            cid=cid)
        module_list.append(this_module)

    return module_list


class Module(DataObject):
    # A module has a name, id, and items_url. It generates CourseItems

    def get_items(self):
        self._items = get_module_items(cid=self.cid, mid=self.mid)
        return self._items

    def __str__(self):
        return '[{0}] {1}'.format(self.id, self.name)

    def __repr__(self):
        return '[{0}] {1}'.format(self.id, self.name)


# return a list of items in module
def get_module_items(cid, mid):
    item_list = []
    url = "%scourses/%s/modules/%s/items%s" % (
        base_url, cid, mid, access_token)
    response = requests.get(url)

    for item in response.json():
        this_item = None
        if item['type'] == 'File':
            # content_id can be used in the download link of a file
            this_item = CourseItem(
                title=item['title'],
                id=item['id'],
                type=item['type'],
                url=item['url'],
                content_id=item['content_id'])
        elif item['type'] == 'Page':
            this_item = CourseItem(
                title=item['title'],
                id=item['id'],
                type=item['type'],
                url=item['url'])
        item_list.append(this_item)
    return item_list


class CourseItem(DataObject):
    # A CourseItem has a title, id, type, and url.
    # If the CourseItem references a file, it also has content_id

    def __str__(self):
        return '[{0}] {1}'.format(self.id, self.title)

    def __repr__(self):
        return '[{0}] {1}'.format(self.id, self.title)


def download_link(content_id):
    link = "%sfiles/%s/download?download_frd=1" % (web_url, content_id)

    return link


def create_page(title, body):
    html_page = """
        <!doctype html>
        <html lang="en">
            <head>
              <meta charset="utf-8">
              <title>%s</title>
            </head>
            %s
        </html>""" % (title, body)
    return html_page

# web_courses_obj = WebcourseObject()
# class_array = web_courses_obj._get_courses()


# for item in class_array:
#     pp.pprint(item.set_modules())
