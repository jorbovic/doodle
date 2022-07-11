import requests
import data
import util

app_url_calendar = data.url + data.calendars


# Get calendar no date
def test_get_calendar_no_date():
    response = requests.get(app_url_calendar)
    util.assert_response_negative(response, 400, data.badRequest, data.calendars)


# Get calendar wrong date format
def test_get_calendar_wrong_date():
    response = requests.get(app_url_calendar + '?month=1983')
    util.assert_response_negative(response, 500, data.internalError, data.calendars)


test_get_calendar_no_date()
test_get_calendar_wrong_date()
