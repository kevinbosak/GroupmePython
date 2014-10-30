#!/usr/bin/python

import pprint
import groupme
from datetime import datetime

token = '7d1fc460f507013114b94e6a4037cf04'
#group_id = '9173535'
group_id='4002754' # xfaction

api = groupme.APIv3(token)
users = api.get_users(group_id=group_id)
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(users)
