import requests
import json
import jsonpath
import data
import util

app_url = data.url + data.slots
startAt = data.slotStartAt
endAt = data.slotEndAt


# Create Slot
def test_create_slot():
    response = requests.post(app_url, json={'startAt': startAt, 'endAt': endAt})
    json_response = json.loads(response.text)
    data.slotID = jsonpath.jsonpath(json_response, 'id')[0]
    util.assert_response_slot(response, 201, startAt, endAt)


# Get Recently Created Slot
def test_get_recently_created_slot():
    response = requests.get(app_url + '/' + data.slotID)
    util.assert_response_slot(response, 200, startAt, endAt)


# Delete Recently Created Slot
def test_delete_recently_created_slot():
    response = requests.delete(app_url + '/' + data.slotID)
    assert response.status_code == 200


# Confirm that Slot is actually deleted
def test_confirm_slot_actually_deleted():
    response = requests.get(app_url + "/" + data.slotID)
    util.assert_response_negative(response, 404, data.notFound, data.slots + '/' + data.slotID)


# Confirm delete status code for already deleted Slot
def test_confirm_status_code_deleted_slot():
    response = requests.delete(app_url + '/' + data.slotID)
    util.assert_response_negative(response, 500, data.internalError, data.slots + '/' + data.slotID)


# Get slots
def test_slot_get():
    response = requests.get(app_url)
    util.assert_get(response, 200, 0, 20)

    # TODO compare response, something similar as is done for test_users_get()


test_create_slot()
test_get_recently_created_slot()
test_delete_recently_created_slot()
test_confirm_slot_actually_deleted()
test_confirm_status_code_deleted_slot()
test_slot_get()
