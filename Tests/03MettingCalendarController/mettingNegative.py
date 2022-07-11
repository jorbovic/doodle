import requests
import data
import util

app_url_meetings = data.url + data.meetings
uid = '00000000-0000-0000-0000-000000000000'


# Create meeting no parameters
def test_create_meeting_no_parameters():
    response = requests.post(app_url_meetings, json={})
    util.assert_response_negative(response, 500, data.internalError, data.meetings)


# Create meeting wrong uid parameters
def test_create_meeting_wrong_uid_parameters():
    response = requests.post(app_url_meetings, json={"slotId": uid, "title": data.meetingTitle, "participants":
        [{"id": uid}]})
    util.assert_response_negative(response, 500, data.internalError, data.meetings)


test_create_meeting_no_parameters()
test_create_meeting_wrong_uid_parameters()