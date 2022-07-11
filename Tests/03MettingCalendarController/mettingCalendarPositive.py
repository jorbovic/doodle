import requests
import json
import jsonpath
import data
import util

app_url_user = data.url + data.users
app_url_slot = data.url + data.slots
app_url_meetings = data.url + data.meetings
app_url_calendar = data.url+data.calendars

# Getting first idSlot, startDateSlot, endDateSlot that will be used for the meeting
response = requests.get(app_url_slot)
json_response = json.loads(response.text)
idSlot = jsonpath.jsonpath(json_response, 'items[0].id')[0]
startDateSlot = jsonpath.jsonpath(json_response, 'items[0].startAt')[0]
endDateSlot = jsonpath.jsonpath(json_response, 'items[0].endAt')[0]

# Getting first userID that will be participants for the meeting
response = requests.get(app_url_user)
json_response = json.loads(response.text)
idUser = jsonpath.jsonpath(json_response, 'items[0].id')[0]


# Create Meeting
def test_create_meeting():
    response = requests.post(app_url_meetings, json={"slotId": idSlot, "title": data.meetingTitle, "participants":
        [{"id": idUser}]})
    json_response = json.loads(response.text)
    data.meetingID = jsonpath.jsonpath(json_response, 'id')[0]
    util.assert_response_meeting(response, 201, data.meetingTitle, startDateSlot, endDateSlot, idUser)


# Get Recently Created Meeting
def test_get_recently_created_meeting():
    response = requests.get(app_url_meetings + "/" + data.meetingID)
    util.assert_response_meeting(response, 200, data.meetingTitle, startDateSlot, endDateSlot, idUser)


# Get meetings
def test_meeting_get():
    response = requests.get(app_url_meetings)
    json_response = json.loads(response.text)

    page = jsonpath.jsonpath(json_response, 'page')[0]
    pageSize = jsonpath.jsonpath(json_response, 'pageSize')[0]
    totalSize = jsonpath.jsonpath(json_response, 'totalSize')[0]

    title = jsonpath.jsonpath(json_response, 'items[0].title')[0]
    startAt = jsonpath.jsonpath(json_response, 'items[0].startAt')[0]
    endAt = jsonpath.jsonpath(json_response, 'items[0].endAt')[0]
    participants = jsonpath.jsonpath(json_response, 'items[0].participants[0].id')[0]

    assert response.status_code == 200
    assert title == data.meetingTitle
    assert startAt == startDateSlot
    assert endAt == endDateSlot
    assert participants == idUser
    assert page == 0
    assert pageSize == 20
    assert totalSize == 1


# Get calendar
def test_get_calendar():
    response = requests.get(app_url_calendar + '?month=1983-07')
    assert response.status_code == 200


# Test that slot is not available because of scheduled meeting
def test_slot_not_available():
    response = requests.get(app_url_slot + '/' + idSlot)
    assert response.status_code == 404


# Delete Recently Created Meeting
def test_delete_recently_created_meeting():
    response = requests.delete(app_url_meetings + "/" + data.meetingID)
    assert response.status_code == 200


# Test that slot is  available because meeting is deleted
def test_slot_available():
    response = requests.get(app_url_slot + '/' + idSlot)
    assert response.status_code == 200


test_create_meeting()
test_get_recently_created_meeting()
test_meeting_get()
test_get_calendar()
test_slot_not_available()
test_delete_recently_created_meeting()
test_slot_available()
