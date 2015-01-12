#!/usr/bin/env python

import groupme
import argparse
import os
from subprocess import check_output
import json

parser = argparse.ArgumentParser(description = 'Gets a list of groups')

parser.add_argument('--token_file',
                    type=str,
                    help='Filename that contains the API token')

parser.add_argument('--save_path',
                    type=str,
                    default='./',
                    help='Path to save the history files in')

parser.add_argument('--save_prefix',
                    type=str,
                    default='',
                    help='Prefix for generating history file names')

parser.add_argument('--group_id',
                    type=int,
                    default=None,
                    help='ID of the group')

args = parser.parse_args()

api = groupme.APIv3(token_file = args.token_file)
groups = []

if args.group_id is not None:
    groups = [api.get_group(args.group_id)]
else:
    groups = api.get_groups()

chat_path = os.path.join(args.save_path, 'chat_list')
print("{} TOTAL GROUPS".format(len(groups)))

for group in groups:
    with open(chat_path, "a") as chat_file:
        chat_file.write(group['id'] + ': ' + group['name'] + '\n')

    last_message_id = None

    # Search for group history file
    filename = args.save_prefix + group['id'] + '.history'
    assert os.path.isdir(args.save_path), 'Save path does not exist'

    full_path = os.path.join(args.save_path, filename)
    last_id = None
    if os.path.isfile(full_path):
        # read last message for the ID
        last_line = check_output(['tail', '-1', full_path])
        if last_line:
            last_message = json.loads(last_line)
            last_message_id = last_message['id']


    with open(full_path, "a") as history_file:
        message_params = {'group_id': group['id'], 'per_page': 100}
        if last_message_id is not None:
            # grab messages up until the message ID last line
            message_params['after_id'] = last_message_id
            messages = api.get_messages(**message_params)
            for message in messages:
                history_file.write(json.dumps(message) + '\n')
        else:
            # grab last 500 of messages, write file
            message_params['maximum'] = 500
            messages = api.get_messages(**message_params)
            for message in reversed(messages):
                history_file.write(json.dumps(message) + '\n')
