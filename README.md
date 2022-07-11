# doodle

RUNNING TESTS:

- Clone the project
- Open it using PyCharm
- Make sure that docker service is running
- Make sure that there are no created meetings
- Make sure that all necessary libraries are installed: requests, json, jsonpath
- Start test from the top to the bottom



FINDINGS:

User
- DELETE user api, for already deleted user returns 500 (internal error) instead of 404 (not found)

Slot
- DELETE slot api, for already deleted slot returns 500 (internal error) instead of 404 (not found)
- POST slot api, is it ok that slots can be created in the past?
- POST slot api, should be there some time range validation? (e.g.: slot not longer than one day)

Meeting
- DELETE meeting api, is returning 200 for already deleted meeting
- POST meeting api, meeting can be created without participants, is that ok?
- POST meeting api, meeting can be created with multiple same participants, is that ok?
- POST meeting api, in case that slot does not exist 500 is returned instead of 404 (slot not found)
- POST meeting api, in case that participants does not exist 500 is returned instead of 404 (participants not found)
- GET meeting api, is not returning slotID parameter for recently added meeting but is should (by documentation)
- GET meetings api, is not returning slotID parameter for recently added meeting but is should (by documentation)

Calendar
- GET calendar api, is returning 500 in case that only year is added, instead of 400 bad request
- GET calendar api, is not returning slotID parameter for recently added meeting but is should (by documentation)

Note:
- Tests will not fail because of findings

What you would do if you had more time:
- Implement assert method where entire json response will be asserted
- Write test different pages, different pages size
- Write more test for some edge cases
