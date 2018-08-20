"""
Slack API Manager
"""
import datetime
from urllib.parse import urljoin, urlencode
from typing import Union

import requests


class SlackApiManager:
    url = 'https://slack.com/api/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def __init__(self, token: str = ''):
        """
        Slack Api Manager
        Args:
            token (str): OAuth Token
        """
        if not token:
            print(
                f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] WARNING: Token is empty (SlackApiManager)')

        # initialize inner class
        self.channel = self.Channel(token)
        self.user = self.User(token)
        self.chat = self.Chat(token)

        self.token = token
        self.headers = SlackApiManager.headers

    def test(self):
        """
        Api test
        Returns:
            bool
        """
        url = urljoin(self.url, './api.test')
        res = requests.post(
            url=url,
            headers=self.headers
        )
        if res.status_code is not 200:
            print(
                f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ERROR: Response not found')
            return False

        return res.json()['ok']

    def is_auth(self):
        """
        Check auth
        Returns:
            bool
        """
        url = urljoin(self.url, './auth.test')
        data = {'token': self.token}
        res = requests.post(
            url=url,
            data=urlencode(data).encode('utf-8'),
            headers=self.headers
        )

        if res.status_code is not 200:
            print(
                f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                f'ERROR: Response not found \'{url}\'')
            return False

        return res.json()['ok']

    class Channel:
        def __init__(self, token: str = ''):
            """
            Slack Channel Api Manager
            Args:
                token (str):
            """
            self.url = SlackApiManager.url
            if not token:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    'WARNING: Token is empty (SlackApiManager.Channel)')

            self.token = token

            self.headers = SlackApiManager.headers

        def history(
                self,
                channel: str = '',
                count: int = 100,
                inclusive: int = 0,
                latest: datetime.datetime = datetime.datetime.now(),
                oldest: int = 0,
                unreads: int = 0):
            """
            fetch channel history
            Args:
                channel (str):
                count (int):
                inclusive (int):
                latest (datetime.datetime):
                oldest (int):
                unreads (int):
            Returns:
                list
            """
            url = urljoin(self.url, './channels.history')

            data = {
                'token': self.token,
                'channel': channel,
                'count': count,
                'inclusive': inclusive,
                'latest': latest,
                'oldest': oldest,
                'unreads': unreads
            }

            res = requests.post(
                url=url,
                data=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: Response not found \'{url}\'')
                return []

            return res.json()['messages']

        def info(self, channel: str = '', include_locale: str = ''):
            url = urljoin(self.url, './channels.info')

            data = {
                'token': self.token,
                'channel': channel,
                'include_locale': include_locale
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: {res.json()["error"]}')
                return {}

            return res.json()['channel']

    class User:
        def __init__(self, token: str = ''):
            """
            Slack User Api Manager
            Args:
                token (str):
            """
            self.url = SlackApiManager.url

            if not token:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    'WARNING: Token is empty (SlackApiManager.User)')

            self.token = token
            self.headers = SlackApiManager.headers

        def info(self, user: str='', include_locale: str=''):
            url = urljoin(self.url, './users.info')

            data = {
                'token': self.token,
                'user': user,
                'include_locale': include_locale
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: {res.json()["error"]}')
                return {}

            return res.json()['user']

        def list(
                self,
                cursor: str='',
                include_locale: str='',
                limit: int=0,
                presence: bool=False):
            url = urljoin(self.url, './users.list')
            data = {
                'token': self.token,
                'cursor': cursor,
                'include_locale': include_locale,
                'limit': limit,
                'presence': presence
            }

            res = requests.post(
                url=url,
                data=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: Response not found \'{url}\'')
                return []

            if not res.json()['ok']:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: {res.json()["error"]}')
                return []

            return res.json()['members']

        def list(
                self,
                cursor: Union[str, None] = None,
                exclude_archived: bool = False,
                exclude_member: bool = False,
                limit: int = 0) -> dict:
            """

            Args:
                cursor (str or None) :
                    Paginate through collections of data by setting the cursor parameter
                    to a next_cursor attribute returned by a previous request's response_metadata.
                    Default value fetches the first "page" of the collection.
                    See [pagination](https://api.slack.com/docs/pagination) for more detail.
                exclude_archived (bool) :
                    Exclude archived channels from the list
                exclude_member (bool):
                    Exclude the members collection from each channel
                limit (int) :
                    The maximum number of items to return.
                    Fewer than the requested number of items may be returned,
                    even if the end of the users list hasn't been reached.

            Returns:
                dict
            """
            url = urljoin(self.url, './channels.list')

            data = {
                'token': self.token,
                'exclude_archived': exclude_archived,
                'exclude_member': exclude_member,
                'limit': limit
            }
            if cursor is not None:
                data.update({'cursor': cursor})

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if not res.json()['ok']:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    f'ERROR: {res.json()["error"]}')
                return {}

            return res.json()['channels']

    class Chat:
        def __init__(self, token: str = ''):
            """
            Slack Chat Api Manager
            Args:
                token (str):
            """
            self.url = SlackApiManager.url
            if not token:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    'WARNING: Token is empty (SlackApiManager.Channel)')

            self.token = token

            self.headers = SlackApiManager.headers

        def postMessage(
                self,
                channel,
                text,
                **kwargs) -> bool:
            """

            Args:
                channel: Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name.
                text: Text of the message to send. This field is usually required, unless you're providing only attachments instead.
                **kwargs: Other API parameters. See below.
                    as_user: Pass true to post the message as the authed user, instead of as a bot.
                    attachments: A JSON-based array of structured attachments, presented as a URL-encoded string.
                    icon_emoji: Emoji to use as the icon for this message. Must be used in conjunction with as_user set to false, otherwise ignored.
                    icon_url: URL to an image to use as the icon for this message.
                    link_names: Find and link channel names and usernames.
                    mrkdwn: Disable Slack markup parsing by setting to false
                    parse: Change how messages are treated.
                    reply_broadcast: Used in conjunction with thread_ts and indicates whether reply should be made visible to everyone in the channel or conversation.
                    thread_ts: Provide another message's ts value to make this message a reply.
                    unfurl_links: Pass true to enable unfurling of primarily text-based content.
                    unfurl_media: Pass false to disable unfurling of media content.
                    username: Set your bot's user name. Must be used in conjunction with as_user set to false, otherwise ignored.

            Returns:
                bool
            """
            url = urljoin(self.url, './chat.postMessage')
            data = {
                'token': self.token,
                'channel': channel,
                'text': text
            }
            if kwargs:
                data.update(kwargs)

            res = requests.post(
                url=url,
                data=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code == 200:
                return True
            return False
