#!/usr/bin/env python

import groupme
import argparse
import pprint

parser = argparse.ArgumentParser(description = 'TEST')

parser.add_argument('--token_file',
                    type=str,
                    help='Filename that contains the API token')

parser.add_argument('--group_id',
                    type=int,
                    help='ID of the group')
args = parser.parse_args()
group_id = args.group_id

api = groupme.APIv3(token_file=args.token_file)
users = api.get_members(group_id=group_id)
for user in users:
    print(user['id'] + ': ' + user['nickname'])
print('TOTAL: {}'.format(len(users)))
