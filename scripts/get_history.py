#!/usr/bin/python

import pprint
import groupme
from datetime import datetime

token = '7d1fc460f507013114b94e6a4037cf04'
#group_id = '9173535'
group_id='4002754' # xfaction

api = groupme.APIv3(token)
count = api.get_message_count(group_id=group_id)
messages = api.get_messages(group_id=group_id, per_page=40, maximum=40, since_id=21103666)

#print("{} TOTAL MESSAGES".format(message_count))
print("Got {} messages of {} total".format(len(messages), count))

users = {}

pp = pprint.PrettyPrinter(indent=2)

#sender_id
#name
#created_at
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
