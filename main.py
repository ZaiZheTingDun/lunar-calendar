import time
import json
import uuid

from icalendar import Calendar, Event
from datetime import datetime
from icalendar import vDatetime
from LunarSolarConverter import LunarSolarConverter


def display(cal1: Calendar) -> str:
    return cal1.to_ical().decode("utf-8").replace('\r\n', '\n').strip()


if __name__ == '__main__':
    with open('example.json') as f:
        data = json.load(f)

        cal = Calendar()
        cal.add('PRODID', 'iCalendar-python')
        cal.add('VERSION', '2.0')

        timestamp = vDatetime(datetime.fromtimestamp(time.time()))


        def create_events(item) -> [Event]:
            def create_event(y: int, m: int, d: int, summary: str) -> Event:
                e = Event()

                converter = LunarSolarConverter.LunarSolarConverter()
                lunar = LunarSolarConverter.Lunar(y, m, d, False)
                solar = converter.LunarToSolar(lunar)

                e.add('UID', uuid.uuid4())
                e.add('DTSTAMP', timestamp)
                e.add('DTSTART', datetime(solar.solarYear, solar.solarMonth, solar.solarDay).date())
                e.add('SUMMARY', summary)

                return e

            date_str: str = item['date']
            summery: str = item['summery']
            years: int = item['years']

            current_year: int = datetime.now().year
            month = int(date_str[0:2])
            day = int(date_str[2:])

            return [create_event(current_year + i, month, day, summery) for i in range(0, years)]


        events = [event for e in data for event in create_events(e)]

        for event in events:
            cal.add_component(event)

        print(display(cal))
