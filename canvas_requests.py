import requests
import data_access_objects


import pprint
pp = pprint.PrettyPrinter(indent=4)


api_key = "13~ai4isuqQYZlTRv6YzBHPIAM05epVD2Fd1e9u7ypHFNjZSEH9xb0JHpWamMUFYngw"
access_token = "?access_token=%s" % (api_key)
web_url = "https://webcourses.ucf.edu/"
base_url = "%sapi/v1/" % (web_url)


# returns the course_id and course_code of Courses available to student
def get_courses():
    course_list = []
    url = "%scourses/%s" % (base_url, access_token)
    # look into prepared response?
    response = requests.get(url)
    for item in response.json(): # response.json() is a list of json objects
        this_course = Course(item['name'], item['id'])
        course_list.append(this_course)

    return course_list

# returns modules in a course based on course_id
def get_modules(cid):
    module_list = []
    url = "%scourses/%s/modules%s" % (base_url, cid, access_token)
    response = requests.get(url)
    for item in response.json():
        module_list.append({item['name'], item['id'], item['items_url']})

    return module_list

# return a list of items in module
def get_moduel_items(cid, mid):
    item_list = []
    url = "%scourses/%s/modules/%s/items%s" % (base_url, cid, mid, access_token)
    response = requests.get(url)

    for item in response.json():
        if item['type'] == 'file':
            # content_id can be used in the download link of a file
            item_list.append({
                item['title'], 
                item['id'], 
                item['type'], 
                item['url'], 
                item['content_id']})
        elif item['type'] == 'Page':
            item_list.append({
                item['title'], 
                item['id'], 
                item['type'], 
                item['url']})
    
    return item_list

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

####################################################################
def test_function():
    url = "https://webcourses.ucf.edu/api/v1/courses/1113951/modules/1290684/items%s" % (access_token)
    response = requests.get(url)
    pp.pprint(response.json())

test_function()