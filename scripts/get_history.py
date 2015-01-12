#!/usr/bin/python

import pprint
import groupme
from datetime import datetime
import argparse

# Currently this script just lists active users but is an example of getting message history and doing something with it

parser = argparse.ArgumentParser(description = 'Get message history for a group')

parser.add_argument('--token_file',
                    type=str,
                    help='Filename that contains the API token')

parser.add_argument('--group_id',
                    type=int,
                    help='ID of the group')

args = parser.parse_args()

api = groupme.APIv3(token_file=args.token_file)
count = api.get_message_count(group_id=args.group_id)
messages = api.get_messages(group_id=args.group_id, per_page=40, maximum=40)

print("Got {} messages of {} total".format(len(messages), count))

users = {}

pp = pprint.PrettyPrinter(indent=2)

for message in messages:
    sender_id = message['sender_id']
    username = message['name']
    created_at = message['created_at']
    dt = datetime.fromtimestamp(int(created_at))
    pretty_time = dt.strftime('%Y-%m-%d %H:%M:%S')

    if users.get(sender_id) is None:
        users[sender_id] = {
            'usernames': [username],
            'last_message_time': pretty_time,
            'last_message': message['text']
        }
    elif username not in users[sender_id]['usernames']:
        users[sender_id]['usernames'].append(username)

pp.pprint(users)
