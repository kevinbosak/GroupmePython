#!/usr/bin/env python

from urllib.parse import urlencode
#import urllib.request
#import urllib.parse
import requests
import json
import sys
import os
import uuid

_BASE_URL = 'https://api.groupme.com/v3'

class APIv3(object):
    """A client for the GroupMe API v3"""

    def __init__(self, token=None, token_file=None):
        assert token is not None or token_file is not None, 'Must specify a token or token file'
        if token is not None:
            self.token = token
        else:
            with open(token_file, 'r') as f:
                # TODO: clean up/validate the token
                self.token = f.read().strip()

    def _make_call(self, url, method, **kwargs):
        response = None

        if method == 'GET':
            kwargs['token'] = self.token
            url = url + '?' + urlencode(kwargs)
            response = requests.get(url)
#            response = urllib.request.urlopen(url)
        else:
            url = url + '?' + urlencode({'token': self.token})
#            body = json.dumps(kwargs).encode('utf-8')
#            body = urllib.parse.urlencode(kwargs).encode('utf-8')
            response = requests.post( url, params=kwargs )

        # TODO: check response.status?
        response_data = {}
        if not response.text or response.text == '':
            response_data['meta'] = {'code': response.status_code}
        else:
            try:
                response_data = response.json()
            except ValueError:
                print("NO JSON IN RESPONSE: " + response.text)

        if response_data['meta']['code'] == 400:
            print('ERRORS: {}'.format(response_data['meta']['errors']))
            quit()

        return {'response': response_data.get('response'), 'response_code': response_data['meta']['code'], 'errors': response_data['meta'].get('errors')}

    def get_members(self, group_id):
        url = _BASE_URL + '/groups/{}'

        response_data = self._make_call(url = url.format(group_id), method = 'GET')
        if response_data['response_code'] == 200:
            return response_data['response']['members']
        return None # TODO: better error handling

    def add_member(self, group_id, nickname, user_id=None, phone_number=None, email=None):
        assert user_id is not None or phone_number is not None or email is not None, 'User ID or Phone or Email is required'
        url = _BASE_URL + '/groups/{}/members/add'
#        guid = str(uuid.uuid4())
        guid = '123403'

#        message_params = {'members': [{"guid": guid, "nickname": nickname, "user_id": str(user_id)}]}
        message_params = {"members": [{
                "guid": guid,
                "nickname": nickname,
                "user_id": str(user_id)}
            ]}
        response_data = self._make_call(url = url.format(group_id), method = 'POST', **message_params)
        if response_data['response_code'] == 202:
            return response_data['response']['results_id']
        return None

    def check_add_member_status(self, group_id, guid):
        url = _BASE_URL + '/groups/{}/members/result/{}'
        response_data = self._make_call(url = url.format(group_id, guid), method = 'GET')

        if response_data['response_code'] == 200:
            return response_data['response']['members']
        return None

    def remove_member(self, group_id, user_id):
        url = '/groups/{}/members/{}/remove'

        response_data = self._make_call(url = url.format(group_id, user_id), method = 'POST')

        if response_data['response_code'] == 200:
            return True
        return False

    # TODO: support attachments
    def create_message(self, group_id, message):
        url = _BASE_URL + '/groups/{}/messages'

        guid = str(uuid.uuid4())

        message_params = {'message': {"source_guid": guid, "text": message}}
        
        response_data = self._make_call(url = url.format(group_id), method = 'POST', **message_params)
        if response_data['response_code'] == 201:
            return response_data['response']['message']['id']
        return None

    def get_message_count(self, group_id):
        url = _BASE_URL + '/groups/{}/messages'
        
        response_data = self._make_call(url = url.format(group_id), method = 'GET', limit = 1)
        if response_data['response_code'] == 200:
            return response_data['response']['count']
        return None

    # TODO: get all message back to a certain date
    def get_messages(self, group_id, maximum=100000, per_page=10, before_id=None, since_id=None, after_id=None):
        url = _BASE_URL + '/groups/{}/messages'

        retrieved = 0

        messages = []
        params = {'limit': per_page}

        while retrieved < maximum:
            if before_id is not None:
                params['before_id'] = before_id
            elif since_id is not None:
                params['since_id'] = since_id
            elif after_id is not None:
                params['after_id'] = after_id

            response_data = self._make_call(url = url.format(group_id), method = 'GET', **params)
            response = response_data['response']
            if response is None or  response.get('messages') is None or len(response['messages']) == 0: # generally when there are no more messages to get break
                return messages

            if after_id is None and since_id is None:
                before_id = response['messages'][-1]['id']
            elif since_id is None and before_id is None:
                after_id = response['messages'][-1]['id']
            elif since_id is not None:
                # TODO:
                # would've gotten the x most recent since ID
                # check for others between the last ID retrieved and since_id?
                break

            retrieved = retrieved + len(response['messages'])
            messages.extend(response['messages'])

        return messages

    def get_group(self, group_id):
        url = _BASE_URL + '/groups/{}'

        group = self._make_call(url = url.format(group_id), method = 'GET')
        return group['response']

    def get_groups(self, maximum=None, per_page=10):
        url = _BASE_URL + '/groups'
        count = 0
        page = 1
        message_params = {'message': {"per_page": per_page, "page": page}}

        groups = []
        
        while True:
            message_params['page'] = page
            response_data = self._make_call(url = url, method = 'GET', **message_params)

            if response_data['response_code'] == 200:
                page_groups = response_data['response']
                if len(page_groups) > 0:
                    groups.extend(page_groups)
                    page = page + 1
                else:
                    return groups
            else:
                return None
        return groups
