import requests


class DataObject(object):
    """
    container object for arbitrary data

    Since using ``namedtuple`` requires knowing the arguments ahead of time,
    this class allows dumping attributes onto the object via keyword args to
    the ``__init__`` arbitrarily.

    NOTE: since it does not subclass a ``collections`` object, it will not
    magically provide iteration or list functionality for the data stored in
    it (not a big deal if you don't need those features), nor does it provide
    immutability like a tuple would.

    NOTE: while this provides flexibility, it doesn't really conform to the
    `Zen of Python <https://www.python.org/dev/peps/pep-0020/>`_
    in being explicit over implicit; ideally, if you wanted to have a data
    container object abstraction in this case, it would probably be better to
    create a separate ``namedtuple`` for each data object you need to
    represent, e.g.:

    .. code-block:: python

        from collections import namedtuple

        CourseData = namedtuple('CourseData', ['id', 'course_id', etc...])
        ModuleData = namedtuple('ModuleData', ['id', 'course_id', etc...])
    """

    def __init__(self, **kwargs):
        """ store provided keywords and values as object attributes """
        for key in kwargs:
            setattr(self, key, kwargs[key])


class WebcourseObject(object):
    """ provides the base object functionality for webcourses paradigms """

    def __init__(self, base_url, course_id, api_key, data=None):
        """
        stores the core information needed for all webcourse objects

        When provided, the raw data from the dict for the object is saved
        into the ``obj`` attribute as a ``DataObject``. Then the
        ``_process_data`` method is called, providing subclasses a way of
        explicitly defining how they handle the raw object data.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.course_id = course_id
        if data is None:
            self.obj = DataObject()
        else:
            self.obj = DataObject(**data)
            self._process_data(data)

    def _process_data(self, data):
        """ provides a hook for explicitly handling raw object data """
        pass


class Module(WebcourseObject):
    """ defines a webcourses module """

    @property
    def items_url(self):
        return '{base}/api/v1/courses/{cid}/modules?access_token={key}'.format(
            base=self.base_url,
            cid=self.course_id,
            key=self.api_key
        )

    def get_items(self):
        pass

    def __str__(self):
        """
        It's almost always a better idea to use string ``.format(...)``
        instead of ``%``-style string interpolation
        """
        return '[{0}] {1}'.format(self.id, self.name)


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
        """
        This is an example of a 'lazy' or 'cached' attribute, i.e. one that
        does something only the first time, then caches the result locally
        on the object, and returns that value whenever subsequently accessed.
        """
        if not hasattr(self, '_modules'):
            return None
        return self._modules

    def get_modules(self):
        """
        While this code could be part of the cached 'modules' attribute, it
        usually is a better idea to put potentially blocking IO operations
        such as HTTP requests somewhere that makes the impact of the operations
        clearer, in this case an actual function call.

        Also note the use of list comprehension to construct the list of
        instantiated ``Module`` objects.
        """
        response = requests.get(self.course_modules_url)
        response_dicts = response.json()
        self._modules = [
            Module(
                self.base_url, self.course_id, self.api_key, data=mod
            ) for mod in response_dicts
        ]
        return self._modules

    def __str__(self):
        """
        It's almost always a better idea to use string ``.format(...)``
        instead of ``%``-style string interpolation
        """
        return '[{0}] {1}'.format(self.id, self.name)


if __name__ == '__main__':
    response = requests.get('someurl')
    with open('filename.html', 'wb') as outfile:
        outfile.write(response.content)