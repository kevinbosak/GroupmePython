#!/usr/bin/env python

import groupme
import argparse
import pprint
import time

parser = argparse.ArgumentParser(description = 'TEST')

parser.add_argument('--token_file',
                    type=str,
                    help='Filename that contains the API token')

parser.add_argument('--group_id',
                    type=int,
                    help='ID of the group')

parser.add_argument('--phone',
                    type=str,
                    default=None,
                    help='Phone Number of the user')

parser.add_argument('--email',
                    type=str,
                    default=None,
                    help='Email Address of the user')

parser.add_argument('--user_id',
                    type=int,
                    default=None,
                    help='ID of the user')

parser.add_argument('--nickname',
                    type=str,
                    help='Nickname of the user')

args = parser.parse_args()
group_id = args.group_id

print(args.user_id)
#assert args.phone is None and args.email is None and args.user_id is None, 'Must specify email, phone or ID'

api = groupme.APIv3(token_file=args.token_file)
guid = api.add_member(group_id=group_id, user_id=args.user_id, nickname=args.nickname, email=args.email, phone_number=args.phone  )
print('GUID: ' + guid)

while True:
    time.sleep(1)
    members = api.check_add_member_status(group_id=group_id, guid=guid)
    if members is not None:
        print(members)
        break
