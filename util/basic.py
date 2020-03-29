import datetime as dt
import time

def get_today_date():
	today_date = dt.date.today().strftime("%Y-%m-%d")
	return today_date

def get_yesterday_date():
	yesterday = dt.date.today() - dt.timedelta(days=1)
	yesterday_date = yesterday.strftime("%Y-%m-%d")
	return yesterday_date

def get_timestamp_utc():
	timestamp_utc=str(dt.datetime.utcnow())
	return timestamp_utc

def get_timestamp_iso():
	timestamp_iso=str(dt.datetime.now(dt.timezone.utc).astimezone().isoformat())
	return timestamp_iso

