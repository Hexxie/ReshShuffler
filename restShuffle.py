from random import shuffle
import sqlite3
import argparse

con = sqlite3.connect("restEvents.db")

cur = con.cursor()

events = [
    "walking on the treadmill",
    "walking outside",
    "grab some coffee in the coffeshop",
    "brew some hand brewed coffee",
    "tea time",
    "abs workout",
    "pull ups",
    "push ups",
    "handstand",
    "headstand",
    "stretching",
    "lay on the bed with closed eyes",
    "lay on the bed with some music",
    "guided meditation"]

def add_event(event, user_id):
    print(f"""INSERT INTO REST_EVENT 
                 (name, counter, last_date, user_id )
                 VALUES ('{event}', '0', NULL, '{user_id}')""")
    cur.execute(f"""INSERT INTO REST_EVENT 
                 (name, counter, last_date, user_id )
                 VALUES ('{event}', '0', NULL, '{user_id}')""")
    con.commit()

def list_all_events():
    res = cur.execute(f"""SELECT USER.name, REST_EVENT.name
                FROM USER INNER JOIN REST_EVENT ON USER.user_id = REST_EVENT.user_id""")
    return [item[1] for item in res.fetchall()]


def list_all_events_dev():
    res = cur.execute("""SELECT USER.name, REST_EVENT.name, REST_EVENT.counter, REST_EVENT.event_id
                FROM USER INNER JOIN REST_EVENT ON USER.user_id = REST_EVENT.user_id""")
    print(res.fetchall())
    

def remove_event(event_id, user_id):
    cur.execute(f"""DELETE FROM REST_EVENT WHERE event_id = '{event_id}' AND user_id = '{user_id}'""")
    con.commit()

def get_shuffled_event():
    all_events = list_all_events()
    shuffle(all_events)
    return all_events[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add')
    parser.add_argument('-l', '--list', action="store_true")
    parser.add_argument('-r', '--rest', action="store_true")
    parser.add_argument('-d', '--delete')

    args = parser.parse_args()

    #print(args)

    if args.list:
        list_all_events_dev()

    if args.add:
        add_event(args.add, 1)

    if args.rest:
        print()
        print(get_shuffled_event())

    if args.delete:
        #provide event_id here
        remove_event(args.delete)