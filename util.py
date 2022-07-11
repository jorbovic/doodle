import re
import json
import jsonpath

UUID_RE = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
DATETIME = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}\+[00]{2}:[0-9]{2}$')


def assert_get(response, status, page, pageSize):
    json_response = json.loads(response.text)

    pageResponse = jsonpath.jsonpath(json_response, 'page')[0]
    pageSizeResponse = jsonpath.jsonpath(json_response, 'pageSize')[0]
    # just confirming that totalSize parameter exist in the response
    jsonpath.jsonpath(json_response, 'totalSize')[0]

    assert response.status_code == status
    assert pageResponse == page
    assert pageSizeResponse == pageSize


def assert_response_negative(response, status, error, path):
    json_response = json.loads(response.text)

    timestamp = jsonpath.jsonpath(json_response, 'timestamp')[0]
    errorResponse = jsonpath.jsonpath(json_response, 'error')[0]
    pathResponse = jsonpath.jsonpath(json_response, 'path')[0]

    assert response.status_code == status
    assert DATETIME.match(timestamp)
    assert errorResponse == error
    assert pathResponse == path


def assert_response_user(response, status, userName):
    json_response = json.loads(response.text)

    userNameResponse = jsonpath.jsonpath(json_response, 'name')[0]
    userId = jsonpath.jsonpath(json_response, 'id')[0]

    assert response.status_code == status
    assert UUID_RE.match(userId)
    assert userNameResponse == userName


def assert_response_slot(response, status, startAt, endAt):
    json_response = json.loads(response.text)
    slotID = jsonpath.jsonpath(json_response, 'id')[0]
    startAtDateResponse = jsonpath.jsonpath(json_response, 'startAt')[0]
    endAtDateResponse = jsonpath.jsonpath(json_response, 'endAt')[0]

    assert response.status_code == status
    assert UUID_RE.match(slotID)
    assert startAtDateResponse == startAt
    assert endAtDateResponse == endAt


def assert_response_meeting(response, status, meetingTitle, startDateSlot, meetingEndAt, idUser):
    json_response = json.loads(response.text)
    meetingID = jsonpath.jsonpath(json_response, 'id')[0]
    meetingTitleResponse = jsonpath.jsonpath(json_response, 'title')[0]
    meetingStartAtResponse = jsonpath.jsonpath(json_response, 'startAt')[0]
    meetingEndAtResponse = jsonpath.jsonpath(json_response, 'endAt')[0]
    meetingParticipantResponse = jsonpath.jsonpath(json_response, 'participants[0].id')[0]

    assert response.status_code == status
    assert UUID_RE.match(meetingID)
    assert meetingTitleResponse == meetingTitle
    assert meetingStartAtResponse == startDateSlot
    assert meetingEndAtResponse == meetingEndAt
    assert meetingParticipantResponse == idUser


