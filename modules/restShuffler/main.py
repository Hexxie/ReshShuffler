import argparse
import sys
import os
import rest_shuffle
from rest_shuffle import Event

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    #subparsers = arg_parser.add_subparsers(help='sub-command help')

    arg_parser.add_argument('-a', '--add')
    arg_parser.add_argument('-l', '--list', choices=['work', 'rest'])
    arg_parser.add_argument('-t', '--today', choices=['work', 'rest'])
    arg_parser.add_argument('-r', '--rest', choices=['work', 'rest'])
    arg_parser.add_argument('-d', '--delete')
    arg_parser.add_argument('-f', '--fill', choices=['work', 'rest'])

    #fill_p = subparsers.add_parser('fill')
   # fill_p.add_argument('work')
    #fill_p.add_argument('rest')

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
        print(args.fill)
        #if os.path.isfile(args.fill):
        #    print(f"File {args.fill} was found")
        #    rest_shuffle.add_events_from_file(args.fill, 1)
        #else:
        #    print("File is not found")
        # Temporary solution
        if args.fill == 'work':
            rest_shuffle.add_events_from_file("../../data/workEvents.txt", 1, 'WORK_EVENT')
        else:
            rest_shuffle.add_events_from_file("../../data/restEvents.txt", 1, 'REST_EVENT')