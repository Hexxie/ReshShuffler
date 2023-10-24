import argparse
import sys
from modules import list_all_events, list_all_events_today, add_event, get_shuffled_event, remove_event

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-a', '--add')
    arg_parser.add_argument('-l', '--list', action="store_true")
    arg_parser.add_argument('-t', '--today', action="store_true")
    arg_parser.add_argument('-r', '--rest', action="store_true")
    arg_parser.add_argument('-d', '--delete')

    if(len(sys.argv) == 1):
        arg_parser.print_help()

    args = arg_parser.parse_args()

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