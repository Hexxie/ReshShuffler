import argparse
import sys
import os
import rest_shuffle
from rest_shuffle import Event

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    #subparsers = arg_parser.add_subparsers(help='sub-command help')

    arg_parser.add_argument('--work', action="store_true")
    arg_parser.add_argument('--rest', action="store_true")
    arg_parser.add_argument('-a', '--add')
    arg_parser.add_argument('-l', '--list', action="store_true")
    arg_parser.add_argument('-t', '--today', action="store_true")
    arg_parser.add_argument('-g', '--get_event', action="store_true")
    arg_parser.add_argument('-d', '--delete')
    arg_parser.add_argument('-f', '--fill')

    if(len(sys.argv) == 1):
        arg_parser.print_help()

    args = arg_parser.parse_args()

    if(not args.work and not args.rest):
        arg_parser.print_help()
        exit()
    elif(args.work and args.rest):
        arg_parser.print_help()
        exit()

    if args.work:
        print("creating work event")
        table_name = 'WORK_EVENT'
        events = Event(1, table_name)
    elif args.rest:
        print("creating rest event")
        table_name = 'REST_EVENT'
        events = Event(1, table_name)

    if args.list:
        print(events.find_all())
    
    if args.today:
        print(events.find_today())

    if args.add:
        events.add(args.add)

    if args.get_event:
        print()
        print(rest_shuffle.get_shuffled_event(1, table_name))

    if args.delete:
        #provide event_id here
        events.remove(args.delete)

    if args.fill:
        if os.path.isfile(args.fill):
            print(f"File {args.fill} was found")
            rest_shuffle.add_events_from_file(args.fill, 1, table_name)
        else:
            print("File is not found")