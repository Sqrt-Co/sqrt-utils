import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError


class SlackNotiBot:
    def __init__(self, channel="noti_test", sender=None):
        try:
            env_file_path = os.path.join(
                os.environ.get("HOME", ""), ".env_sqrt", ".env"
            )
            load_dotenv(env_file_path)
        except FileNotFoundError:
            # .env file does not exist but it's okay if you have env variables set
            pass

        slack_token = os.environ.get("SLACK_API_TOKEN")

        if slack_token is None:
            raise ValueError("SLACK_API_TOKEN environment variable is not set")

        self._channel = channel
        self._sender = sender
        self._slack_client = WebClient(token=slack_token)
        self._async_slack_client = AsyncWebClient(token=slack_token)

    def _display_sender(self, text):
        if self._sender is not None:
            # text = f"{self._sender} > {text}"
            text = f"{self._sender} &gt; {text}"

        text = "*" * 100 + "\n" + text
        text += "\n" + "*" * 100

        return text

    async def send_to_slack_async(self, text):
        try:
            text = self._display_sender(text)
            # Don't forget to have await as the client returns asyncio.Future
            response = await self._async_slack_client.chat_postMessage(
                channel=self._channel, text=text
            )
            # assert response["message"]["text"] == text
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            raise e

    def send_to_slack(self, text):
        try:
            text = self._display_sender(text)
            response = self._slack_client.chat_postMessage(
                channel=self._channel, text=text
            )
            # assert response["message"]["text"] == text
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            raise e


async def async_main():
    bot = SlackNotiBot(sender="Jin")
    bot.send_to_slack("동기적 메시징 함수")
    await bot.send_to_slack_async("비동기적 메시징 함수")


if __name__ == "__main__":
    import asyncio

    asyncio.run(async_main())
