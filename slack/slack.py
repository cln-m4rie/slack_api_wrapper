"""
Slack API Manager
"""
import datetime
from urllib.parse import urljoin, urlencode

import requests
from typing import Union
from .utils import Functions


class SlackApiManager:
    url = 'https://slack.com/api/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    logger = Functions.PrintFunc()

    def __init__(self, token: str):
        """
        Slack Api Manager
        Args:
            token (str):
        """
        self.logger = SlackApiManager.logger

        if not token:
            self.logger.warning('Token is empty (SlackApiManager)')

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
            self.logger.warning('Response not found')
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
            self.logger.warning('Response not found \'{url}\'')
            return False

        return res.json()['ok']

    class Channel:
        def __init__(self, token: str):
            """
            Slack Channel Api Manager

            Args:
                token (str) : Authentication token bearing required scopes.
            """
            if not token:
                self.logger.warning('Token is empty (SlackApiManager)')

            self.logger = SlackApiManager.logger
            self.url = SlackApiManager.url
            self.token = token
            self.headers = SlackApiManager.headers

        def archive(self, channel: str) -> bool:
            """

            Args:
                channel (str) : channel to archive

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is emtpy.')

            url = urljoin(self.url, './channels.archive')

            data = {
                'token': self.token,
                'channel': channel
            }

            res = requests.post(
                url=url,
                data=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning('Response not found \'{url}\'')
                return False

            if res.json()['ok'] is False:
                self.logger.warning(f'{res.json()["error"]}')

            return res.json()['ok']

        def create(self, name: str, validate: bool = True) -> dict:
            """

            Args:
                name (str) :
                    Name of channel to create
                validate (bool) :
                    Whether to return errors on invalid channel name
                    instead of modifying it to meet the specified criteria.

            Returns:
                dict
            """
            if not name:
                raise ValueError('name is empty.')

            url = urljoin(self.url, './channels.create')

            data = {
                'token': self.token,
                'name': name,
                'validate': validate
            }

            res = requests.post(
                url=url,
                data=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning('Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')

            return res.json()['channel']

        def history(
                self,
                channel: str,
                count: int = 100,
                inclusive: int = 0,
                latest: datetime.datetime = datetime.datetime.now(),
                oldest: int = 0,
                unreads: int = 0) -> list:
            """

            Args:
                channel (str):
                    Channel to fetch history for.
                count (int):
                    Number of messages to return, between 1 and 1000.
                inclusive (int):
                    Include messages with latest or oldest timestamp in results.
                latest (datetime.datetime):
                    End of time range of messages to include in results.
                oldest (int):
                    Start of time range of messages to include in results.
                unreads (int):
                    Include unread_count_display in the output?

            Returns:
                list
            """
            if not channel:
                raise ValueError('channel is emtpy.')

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
                self.logger.warning(f'Response not found \'{url}\'')
                return []

            return res.json()['messages']

        def info(self, channel: str, include_locale: bool = False) -> dict:
            """

            Args:
                channel (str) :
                    Channel to get info on.
                include_locale (bool) :
                    Set this to true to receive the locale for this channel. Defaults to false.

            Returns:
                dict
            """
            if not channel:
                raise ValueError('channel is emtpy.')

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
                self.logger.warning(f'Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return {}

            return res.json()['channel']

        def invite(self, channel: str, user: str) -> dict:
            """

            Args:
                channel (str) :
                    Channel to invite user to.
                user (str) :
                    User to invite to channel.

            Returns:
                dict
            """
            if not channel:
                raise ValueError('Channel is empty.')
            if not user:
                raise ValueError('User is empty.')

            url = urljoin(self.url, './channels.invite')

            data = {
                'token': self.token,
                'channel': channel,
                'user': user
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return {}

            return res.json()['channel']

        def join(self, name: str, validate: bool = True) -> dict:
            """

            Args:
                name (str) :
                    Name of channel to join
                validate (bool) :
                    Whether to return errors on invalid channel name
                    instead of modifying it to meet the specified criteria.

            Returns:
                dict
            """
            if not name:
                raise ValueError('name is empty.')

            url = urljoin(self.url, './channels.join')

            data = {
                'token': self.token,
                'name': name,
                'validate': validate
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return {}

            return res.json()['channel']

        def kick(self, channel: str, user: str) -> bool:
            """

            Args:
                channel (str) :
                    Channel to remove user from.
                user (str) :
                    User to remove from channel.

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is empty.')
            if not user:
                raise ValueError('user is empty.')

            url = urljoin(self.url, './channels.kick')

            data = {
                'token': self.token,
                'channel': channel,
                'user': user
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return False

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return False

            return res.json()['ok']

        def leave(self, channel: str) -> bool:
            """

            Args:
                channel (str) : Channel to leave

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is empty.')

            url = urljoin(self.url, './channels.leave')

            data = {
                'token': self.token,
                'channel': channel
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return False

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return False

            return res.json()['ok']

        def replies(self, channel: str, thread_ts: str) -> list:
            """

            Args:
                channel (str) :
                    Channel to fetch thread from
                thread_ts (str) :
                    Unique identifier of a thread's parent message

            Returns:
                list
            """
            if not channel:
                raise ValueError('channel is emtpy.')
            if not thread_ts:
                raise ValueError('thread_ts is emtpy.')

            url = urljoin(self.url, './channels.replies')

            data = {
                'token': self.token,
                'channel': channel,
                'thread_ts': thread_ts
            }

            res = requests.post(
                url=url,
                data=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return []

            return res.json()['messages']

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
                self.logger.warning(f'{res.json()["error"]}')
                return {}

            return res.json()['channels']

        def mark(self, channel: str, ts: str) -> bool:
            """

            Args:
                channel (str) :
                    Channel to set reading cursor in.
                ts (str) :
                    Timestamp of the most recently seen message.

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is empty.')
            if not ts:
                raise ValueError('ts (timestamp) is empty.')

            url = urljoin(self.url, './channels.mark')

            data = {
                'token': self.token,
                'channel': channel,
                'ts': ts
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return False

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return False

            return res.json()['ok']

        def rename(self, channel: str, name: str,
                   validate: bool = True) -> dict:
            """

            Args:
                channel (str) :
                    Channel to rename
                name (str) :
                    New name for channel.
                validate (bool) :
                    Whether to return errors on invalid channel name
                    instead of modifying it to meet the specified criteria.

            Returns:
                dict
            """
            if not channel:
                raise ValueError('channel is empty.')
            if not name:
                raise ValueError('name is emtpy.')

            url = urljoin(self.url, './channels.rename')

            data = {
                'token': self.token,
                'channel': channel,
                'name': name,
                'validate': validate
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return {}

            return res.json()['channel']

        def setPurpose(self, channel: str, purpose: str) -> bool:
            """

            Args:
                channel (str) :
                    Channel to set the purpose of
                purpose (str) :
                    The new purpose

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is empty.')
            if not purpose:
                raise ValueError('purpose is empty.')

            url = urljoin(self.url, './channels.setPurpose')

            data = {
                'token': self.token,
                'channel': channel,
                'purpose': purpose
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return False

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return False

            return res.json()['ok']

        def setTopic(self, channel: str, topic: str) -> bool:
            """

            Args:
                channel (str) :
                    Channel to set the topic of
                topic (str) :
                    The new topic

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is empty.')
            if not topic:
                raise ValueError('topic is empty')

            url = urljoin(self.url, './channels.setTopic')

            data = {
                'token': self.token,
                'channel': channel,
                'topic': topic
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return False

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return False

            return res.json()['ok']

        def unarchive(self, channel: str) -> bool:
            """

            Args:
                channel (str) : Channel to unarchive

            Returns:
                bool
            """
            if not channel:
                raise ValueError('channel is empty.')

            url = urljoin(self.url, './channels.unarchive')

            data = {
                'token': self.token,
                'channel': channel
            }

            res = requests.get(
                url=url,
                params=urlencode(data).encode('utf-8'),
                headers=self.headers
            )

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return False

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return False

            return res.json()['ok']

    class Chat:
        def __init__(self, token: str):
            """
            Slack Chat API Manager
            Args:
                token (str) : Authentication token bearing required scopes.
            """
            self.logger = SlackApiManager.logger
            self.url = SlackApiManager.url

            if not token:
                self.logger.warning('Token is empty (SlackApiManager.Channel)')

            self.token = token
            self.headers = SlackApiManager.headers

        def postMessage(
                self,
                channel,
                text,
                **kwargs) -> dict:
            """

            Args:
                channel:
                    Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name.
                text:
                    Text of the message to send. This field is usually required,
                    unless you're providing only attachments instead.
                **kwargs: Other API parameters. See below.
                    as_user:
                        Pass true to post the message as the authenticated user, instead of as a bot.
                    attachments:
                        A JSON-based array of structured attachments, presented as a URL-encoded string.
                    icon_emoji:
                        Emoji to use as the icon for this message.
                        Must be used in conjunction with as_user set to false, otherwise ignored.
                    icon_url:
                        URL to an image to use as the icon for this message.
                    link_names:
                        Find and link channel names and usernames.
                    mrkdwn:
                        Disable Slack markup parsing by setting to false
                    parse:
                        Change how messages are treated.
                    reply_broadcast:
                        Used in conjunction with thread_ts and indicates
                        whether reply should be made visible to everyone in the channel or conversation.
                    thread_ts:
                        Provide another message's ts value to make this message a reply.
                    unfurl_links:
                        Pass true to enable unfurling of primarily text-based content.
                    unfurl_media:
                        Pass false to disable unfurling of media content.
                    username:
                        Set your bot's user name.
                        Must be used in conjunction with as_user set to false, otherwise ignored.

            Returns:
                dict
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

            if res.status_code is not 200:
                self.logger.warning(f'Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return {}

            return res.json()

    class User:
        def __init__(self, token: str):
            """
            Slack User Api Manager

            Args:
                token (str) : Authentication token bearing required scopes.
            """
            self.logger = SlackApiManager.logger

            if not token:
                print(
                    f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '
                    'WARNING: Token is empty (SlackApiManager.User)')

            self.url = SlackApiManager.url
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
                self.logger.warning(f'Response not found \'{url}\'')
                return {}

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
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
                self.logger.warning(f'Response not found \'{url}\'')
                return []

            if not res.json()['ok']:
                self.logger.warning(f'{res.json()["error"]}')
                return []

            return res.json()['members']
