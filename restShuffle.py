from random import shuffle
import sqlite3
import argparse
import datetime
from dateutil import parser

con = sqlite3.connect("restEvents.db")

cur = con.cursor()

def add_event(event, user_id):
    print(f"""INSERT INTO REST_EVENT 
                 (name, counter, last_date, user_id )
                 VALUES ('{event}', '0', NULL, '{user_id}')""")
    cur.execute(f"""INSERT INTO REST_EVENT 
                 (name, counter, last_date, user_id )
                 VALUES ('{event}', '0', NULL, '{user_id}')""")
    con.commit()

def list_all_events():
    res = cur.execute(f"""SELECT USER.name, REST_EVENT.name, REST_EVENT.counter, REST_EVENT.event_id, REST_EVENT.last_date
                FROM USER INNER JOIN REST_EVENT ON USER.user_id = REST_EVENT.user_id""")
    #return [item[1] for item in res.fetchall()]
    return res.fetchall()

def list_all_events_today():
    res = cur.execute("""SELECT USER.name, REST_EVENT.name, REST_EVENT.counter, REST_EVENT.event_id, REST_EVENT.last_date
                FROM USER INNER JOIN REST_EVENT ON USER.user_id = REST_EVENT.user_id""")
    events = res.fetchall()
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

def remove_event(event_id, user_id):
    cur.execute(f"""DELETE FROM REST_EVENT WHERE event_id = '{event_id}' AND user_id = '{user_id}'""")
    con.commit()

def update_event(user_id, event_id, counter, date):
    cur.execute(f"""UPDATE REST_EVENT 
                SET counter = '{counter}', last_date = '{date}'
                WHERE event_id = '{event_id}' AND user_id = '{user_id}'""")
    con.commit()

def get_shuffled_event(user_id):
    all_events = list_all_events_today()
    if not all_events:
        return "I run out of the events. You can choose whatever you want!"
    shuffle(all_events)
    chosen_event = all_events[0]
    print(chosen_event)

    #This is how to update an event with date and counter (I want to know how often I get particular events)
    count = chosen_event[2] + 1
    event_id = chosen_event[3]
    event_name = chosen_event[1]
    update_event(user_id, event_id, count, datetime.datetime.now())
    return event_name

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-a', '--add')
    arg_parser.add_argument('-l', '--list', action="store_true")
    arg_parser.add_argument('-t', '--today', action="store_true")
    arg_parser.add_argument('-r', '--rest', action="store_true")
    arg_parser.add_argument('-d', '--delete')

    args = arg_parser.parse_args()

    #print(args)

    if args.list:
        print(list_all_events())
    
    if args.today:
        print(list_all_events_today())

    if args.add:
        add_event(args.add, 1)

    if args.rest:
        print()
        print(get_shuffled_event(1))

    if args.delete:
        #provide event_id here
        remove_event(args.delete, 1)