import requests
import json
import jsonpath
import data
import util

app_url = data.url + data.slots
beforeAt = data.slotBeforeAt
startAt = data.slotStartAt
middleAt = data.sLotMiddleAt
endAt = data.slotEndAt
afterAt = data.slotAfterAt


# Create slot no parameter
def test_slot_no_parameter():
    response = requests.post(app_url, json={})
    util.assert_response_negative(response, 500, data.internalError, data.slots)


# Create slot no startAt parameter
def test_slot_no_startAt():
    response = requests.post(app_url, json={"startAt": startAt})
    util.assert_response_negative(response, 500, data.internalError, data.slots)


# Create slot no endAt parameter
def test_slot_no_endAt():
    response = requests.post(app_url, json={"endAt": startAt})
    util.assert_response_negative(response, 500, data.internalError, data.slots)


# Create slot incorrect parameter name
def test_slot_incorrect_parameter():
    response = requests.post(app_url, json={"startAtt": endAt, "endAtt": startAt})
    util.assert_response_negative(response, 500, data.internalError, data.slots)


# Create slot where startTime > endTime
def test_slot_starTime_after_endTime():
    response = requests.post(app_url, json={"startAt": endAt, "endAt": startAt})
    util.assert_response_negative(response, 500, data.internalError, data.slots)


# Create slot where startTime = endTime
def test_slot_starTime_equal_endTime():
    response = requests.post(app_url, json={"startAt": startAt, "endAt": startAt})
    util.assert_response_negative(response, 500, data.internalError, data.slots)


# Create slot
def test_create_slot():
    response = requests.post(app_url, json={"startAt": startAt, "endAt": endAt})
    json_response = json.loads(response.text)
    data.slotID = jsonpath.jsonpath(json_response, 'id')[0]
    assert response.status_code == 201


# Crate slot with same date
def test_create_slot_same_date():
    response = requests.post(app_url, json={"startAt": startAt, "endAt": endAt})
    util.assert_response_negative(response, 409, data.conflict, data.slots)


# Create slot with occupied startAt
def test_create_slot_occupied_startAt():
    response = requests.post(app_url, json={"startAt": middleAt, "endAt": endAt})
    util.assert_response_negative(response, 409, data.conflict, data.slots)


# Create slot with occupied endAt
def test_create_slot_occupied_endAt():
    response = requests.post(app_url, json={"startAt": beforeAt, "endAt": middleAt})
    util.assert_response_negative(response, 409, data.conflict, data.slots)


# Create slot with occupied startAt and endAt
def test_create_slot_occupied_startAt_and_endAt():
    response = requests.post(app_url, json={"startAt": beforeAt, "endAt": afterAt})
    util.assert_response_negative(response, 409, data.conflict, data.slots)


# Delete recently created slot
def test_delete_recently_created_slot():
    response = requests.delete(app_url + "/" + data.slotID)
    assert response.status_code == 200


# Get slot wrong uid parameter
def test_get_recently_created_slot():
    response = requests.get(app_url + '/0000')
    util.assert_response_negative(response, 400, data.badRequest, data.slots + "/0000")


test_slot_no_parameter()
test_slot_no_startAt()
test_slot_no_endAt()
test_slot_incorrect_parameter()
test_slot_starTime_after_endTime()
test_slot_starTime_equal_endTime()
test_create_slot()
test_create_slot_same_date()
test_create_slot_occupied_startAt()
test_create_slot_occupied_endAt()
test_create_slot_occupied_startAt_and_endAt()
test_delete_recently_created_slot()
test_get_recently_created_slot()
