import argparse
import sys
import os
import rest_shuffle
from rest_shuffle import Event

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-a', '--add')
    arg_parser.add_argument('-l', '--list', action="store_true")
    arg_parser.add_argument('-t', '--today', action="store_true")
    arg_parser.add_argument('-r', '--rest', action="store_true")
    arg_parser.add_argument('-d', '--delete')
    arg_parser.add_argument('-f', '--fill')

    if(len(sys.argv) == 1):
        arg_parser.print_help()

    args = arg_parser.parse_args()

    events = Event()

    if args.list:
        print(events.find_all())
    
    if args.today:
        print(events.find_today())

    if args.add:
        events.add(args.add)

    if args.rest:
        print()
        print(rest_shuffle.get_shuffled_event(1))

    if args.delete:
        #provide event_id here
        events.remove(args.delete)

    if args.fill:
        if os.path.isfile(args.fill):
            print(f"File {args.fill} was found")
            rest_shuffle.add_events_from_file(args.fill, 1)
        else:
            print("File is not found")