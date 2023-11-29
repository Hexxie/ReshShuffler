import datetime
import sqlite_db
from dateutil import parser
from random import shuffle

class User:
    def __init__(self, telegram_id = None, user_id = 1):
        self._cur = sqlite_db.db.get_cursor()
        self._con = sqlite_db.db.get_connection()
        self.telegram_id = telegram_id
        self.user_id = user_id
        self.name = "default"
        self.is_exists = False

        if telegram_id is not None:
            res = self.find_by_telegram_id()
            if res:
                self.user_id = res[0][0]
                self.name = res[0][1]
                self.is_exists = True

    def add(self, name, telegram_id = None):
        res = self._cur.execute(f"SELECT telegram_id from USER WHERE telegram_id = {telegram_id}")
        if not res.fetchall():
            print(f"""INSERT INTO USER
                        (name, telegram_id )
                        VALUES ('{name}','{telegram_id}')""")
            self._cur.execute(f"""INSERT INTO USER 
                        (name, telegram_id )
                        VALUES ('{name}','{telegram_id}')""")
            self._con.commit()
            self.name = name
            self.telegram_id = telegram_id

    def find_by_telegram_id(self):
        res = self._cur.execute(f"""
                                SELECT user_id, name from USER
                                WHERE telegram_id = '{self.telegram_id}'""")
        data = res.fetchall()
        print(f"the list {data}")
        return data

class Event:
    def __init__(self, user_id = 1, table='REST_EVENT'):
        self.user_id = user_id
        self.table = table
        self._cur = sqlite_db.db.get_cursor()
        self._con = sqlite_db.db.get_connection()

    def add(self, event):
        res = self._cur.execute(f"SELECT user_id from USER WHERE user_id = {self.user_id}")
        if not res.fetchall():
            print("User not found")
        else:
            print(f"""INSERT INTO {self.table} 
                        (name, counter, last_date, user_id )
                        VALUES ('{event}', '0', NULL, '{self.user_id}')""")
            self._cur.execute(f"""INSERT INTO {self.table} 
                        (name, counter, last_date, user_id )
                        VALUES ('{event}', '0', NULL, '{self.user_id}')""")
            self._con.commit()

    def update(self, event_id, counter, date):
        self._cur.execute(f"""UPDATE {self.table} 
                SET counter = '{counter}', last_date = '{date}'
                WHERE event_id = '{event_id}' AND user_id = '{self.user_id}'""")
        self._con.commit()

    def remove(self, event_id):
        self._cur.execute(f"""DELETE FROM {self.table} WHERE event_id = '{event_id}' AND user_id = '{self.user_id}'""")
        self._con.commit()

    def find_all(self):
        print(self.table)
        res = self._cur.execute(f"""
                                SELECT USER.name, {self.table}.name, {self.table}.counter, {self.table}.event_id, {self.table}.last_date
                                FROM USER 
                                INNER JOIN {self.table} ON USER.user_id = {self.table}.user_id
                                WHERE USER.user_id = '{self.user_id}'""")
        return res.fetchall()
    
    def find_today(self):
        events = self.find_all()
        #Remove events with today's date from the list to exclude them from shuffling
        for item in events.copy():
            try:
                date_str = item[4]
                event_date = parser.parse(date_str)
                if(event_date.date() == datetime.date.today()):
                    events.remove(item)
            except TypeError:
                continue
        return events


def get_shuffled_event(user_id, table='REST_EVENT'):
    events = Event(user_id, table)
    all_events = events.find_today()
    if not all_events:
        return "I run out of the events. You can choose whatever you want!"
    shuffle(all_events)
    chosen_event = all_events[0]
    print(chosen_event)

    #This is how to update an event with date and counter (I want to know how often I get particular events)
    count = chosen_event[2] + 1
    event_id = chosen_event[3]
    event_name = chosen_event[1]
    events.update(event_id, count, datetime.datetime.now())
    return event_name

def add_events_from_file(file, user_id, table):
    events = Event(user_id, table)
    with open(file) as f:
        [events.add(line) for line in f.readlines()]

if __name__ == '__main__':
    #to run from the shortcut
    print()
    print(get_shuffled_event(1))
    x = input()
    user = User(123)
    print(user.find_by_telegram_id(123))