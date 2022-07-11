import requests
import data
import util

app_url = data.url + data.users


# Create user no parameters
def test_create_user_no_parameter_name():
    response = requests.post(app_url, json={})
    util.assert_response_negative(response, 500, data.internalError, data.users)


# Create user incorrect parameter name
def test_create_user_incorrect_parameter_name():
    response = requests.post(app_url, json={'namee': data.userName})
    util.assert_response_negative(response, 500, data.internalError, data.users)


# Get user wrong uid parameter
def test_get_user_incorrect_parameter_name():
    response = requests.get(app_url + "/0000")
    util.assert_response_negative(response, 400, data.badRequest, data.users + "/0000")


# Delete user no uid parameter
def test_confirm_status_code_deleted_user():
    response = requests.delete(app_url)
    util.assert_response_negative(response, 405, data.methodNotAllowed, data.users)


test_create_user_no_parameter_name()
test_create_user_incorrect_parameter_name()
test_get_user_incorrect_parameter_name()
test_confirm_status_code_deleted_user()

