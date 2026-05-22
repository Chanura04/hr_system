# from gcsa.google_calendar import GoogleCalendar

# calendar = GoogleCalendar(
#     credentials_path="credentials.json",
#     token_path="token.json",
#     open_browser=True
# )

# print(list(calendar.get_events()))

import requests

r = requests.get("https://www.googleapis.com")

print(r.status_code)