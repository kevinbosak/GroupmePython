#!/usr/bin/env python

import groupme
import argparse

parser = argparse.ArgumentParser(description = 'Gets a list of groups')

parser.add_argument('--token_file',
                    type=str,
                    help='Filename that contains the API token')

parser.add_argument('--group_id',
                    type=str,
                    help='Group ID to retrieve')

args = parser.parse_args()

api = groupme.APIv3(token_file = args.token_file)
data = api.get_group(args.group_id)

print(data)
