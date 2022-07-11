import requests
import json
import jsonpath
import data
import util

app_url = data.url + data.users


# Create User
def test_create_user():
    response = requests.post(app_url, json={'name': data.userName})
    json_response = json.loads(response.text)
    data.userID = jsonpath.jsonpath(json_response, 'id')[0]
    util.assert_response_user(response, 201, data.userName)


# Get Recently Created User
def test_get_created_user():
    response = requests.get(app_url + "/" + data.userID)
    util.assert_response_user(response, 200, data.userName)


# Delete Recently Created User
def test_delete_created_user():
    response = requests.delete(app_url + '/' + data.userID)
    assert response.status_code == 200


# Confirm that user is actually deleted
def test_confirm_deleted_user():
    response = requests.get(app_url + '/' + data.userID)
    path = data.users + '/' + data.userID
    util.assert_response_negative(response, 404, data.notFound, path)


# Confirm delete status code for already deleted user
def test_confirm_status_code_deleted_user():
    response = requests.delete(app_url + "/" + data.userID)
    path = data.users + '/' + data.userID
    util.assert_response_negative(response, 500, data.internalError, path)


# Get users
def test_users_get():
    response = requests.get(app_url)
    util.assert_get(response, 200, 0, 20)
    json_response = json.loads(response.text)

    for i in range(0, 20):
        # just confirming that name parameter exist in the response
        jsonpath.jsonpath(json_response, 'items[' + str(i) + '].name')[0]
        id = jsonpath.jsonpath(json_response, 'items[' + str(i) + '].id')[0]
        assert util.UUID_RE.match(id)

    util.assert_get(response, 200, 0, 20)


test_create_user()
test_get_created_user()
test_delete_created_user()
test_confirm_deleted_user()
test_confirm_status_code_deleted_user()
test_users_get()
