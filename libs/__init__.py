#!/usr/bin/env python

from urllib.parse import urlencode
import urllib.request
import json
import sys
import uuid

_BASE_URL = 'https://api.groupme.com/v3'

_BASE_URLS = {
    'groups': {
        'URL': '/groups',
        'METHOD': 'GET' },
    'members': {
        'URL': '/members',
        'METHOD': 'GET' },
    'messages': {
        'URL': '/groups/{}/messages',
        'METHOD': 'GET' },
    'direct_messages': {
        'URL': '/direct_messages',
        'METHOD': 'GET' },
    'bots': {
        'URL': '/bots',
        'METHOD': 'POST' },
    'user': {
        'URL': '/users/me',
        'METHOD': 'GET' }
    }

class APIv3(object):
    """A client for the GroupMe API v3"""

    def __init__(self, token=None):
        self.token = token

    def _make_call(self, url=None, method=None, **kwargs):
        response = None

        if method == 'GET':
            kwargs['token'] = self.token
            url = url + '?' + urlencode(kwargs)
            response = urllib.request.urlopen(url)
        else:
            url = url + '?' + urlencode({'token': token})
            body = json.dumps(kwargs)
            response = urllib.request.urlopen(url, data=body)

        # TODO: check response.status?
        response_data = json.loads(response.read().decode("utf-8"))
        print('STATUS: {}'.format(response.status))

        if (response_data['meta']['code'] != '200' and response['meta']['code'] != 201):
            return response_data['response']
        else:
            return None

    def get_users(self, group_id=None):
        url_info = _BASE_URLS['groups']
        url = _BASE_URL + url_info['URL'] + '/{}'

        response = self._make_call(url = url.format(group_id), method = url_info['METHOD'],)
        params = {'limit': per_page}
        return response

    # TODO: support attachments
    def create_message(self, group_id=None, message=None):
        url_info = _BASE_URLS['messages']
        url = _BASE_URL + url_info['URL']

        uuid = str(uuid.uuid4())

        message_params = {message: {"source_guid": guid, text: message}
        
        response = self._make_call(url = url.format(group_id), method = 'POST', **message_params)
        return response['message']['id']

    def get_message_count(self, group_id=None):
        url_info = _BASE_URLS['messages']
        url = _BASE_URL + url_info['URL']
        
        response = self._make_call(url = url.format(group_id), method = url_info['METHOD'], limit = 1)
        return response['count']

    # TODO: get all message back to a certain date
    def get_messages(self, group_id=None, maximum=None, per_page=10, before_id=None, since_id=None, after_id=None):
        url_info = _BASE_URLS['messages']
        url = _BASE_URL + url_info['URL']

        retrieved = 0
        total_messages  = self.get_message_count(group_id)
        if maximum is None:
            maximum = total_messages

        messages = []
        params = {'limit': per_page}

        while retrieved < maximum and retrieved < total_messages:
            if before_id is not None:
                params['before_id'] = before_id
            elif since_id is not None:
                params['since_id'] = since_id
            elif since_id is not None:
                params['after_id'] = after_id

            response = self._make_call(url = url.format(group_id), method = url_info['METHOD'], **params)
            if response is None: # generally when there are no more messages to get
                break

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
