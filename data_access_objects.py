import requests

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
        self.errors = False
        # return array of Course objects
        self.course_list = self.get_courses()

    def get_courses(self):
        course_list = []
        url = "%scourses/%s" % (base_url, access_token)
        response = requests.get(url)  # look into prepared response?
        if response.status_code == 200:
            for item in response.json():
                # response.json() is a list of json objects
                this_course = Course(
                    name=item['name'],
                    id=item['id'])
                course_list.append(this_course)
        else:
            self.errors = True
            self.code = response.status_code
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
        return '[{0}] {1}'.format(self.type, self.name)

    @classmethod
    def from_url(cls, url, expect_json=True):

        response = requests.get(url + access_token)

        if expect_json:
            data = response.json()
        else:
            data = {'raw': response.content()}

        params = {}
        if 'body' in data:
            params['type'] = 'page'
            params['name'] = data['title']
            params['body'] = data['body']
            params['filename'] = data['url']
        else:
            params['type'] = 'file'
            params['name'] = data['display_name']
            params['filename'] = data['filename']
            params['content_type'] = data['content-type']
            params['url'] = data['url']
            params['thumbnail_url'] = data['thumbnail_url']
            params['size'] = data['size']

        return cls(**params)

    @property
    def html(self):
        html_template = unicode((
            '<!doctype html>'
            '<html lang="en">'
            '    <head>'
            '        <meta charset="utf-8">'
            '        <title>{title}</title>'
            '    </head>'
            '    {body}'
            '</html>'),
            encoding='utf-8'
        )
        if not hasattr(self, '_html'):
            if not hasattr(self, 'body'):
                raise ValueError('missing body attirubte for html')
            if not hasattr(self, 'name'):
                raise ValueError('missing name attirubte of html')
            self._html = html_template.format(
                title=self.name,
                body=self.body
            )
        return self._html

    @property
    def file_path(self):
        if not hasattr(self, '_file_path'):
            if self.type == 'page':
                self._file_path = 'files/{0}.html'.format(self.name)
            else:
                self._file_path = 'files/{0}'.format(self.filename)

        return self._file_path

    # can set a max size
    def item_content(self, cache=False):
        if self.type == 'page':
            content = self.html.encode('utf-8')
        elif hasattr(self, '_raw'):
            content = self._raw
        else:
            response = requests.get(self.url)
            if cache is True:
                self._raw = response.content
            content = response.content
        # if isinstance(content, unicode):
        #     content = bytes(content, 'utf-8')
        return content
