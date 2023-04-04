# sqrt-util
Utilities for SqRT

to install
`pip install git+ssh://git@github.com/Sqrt-Co/sqrt-utils.git@main`

you need .env file in `{YOUR_HOME}/.env_sqrt/.env`


### Simple Usage for SlackNotiBot
```
from sqrt_utils.logging.slack_bot import SlackNotiBot


def main():
    bot = SlackNotiBot(channel="noti_test", sender="Jin")
    bot.send_to_slack("example message")


async def async_main():
    bot = SlackNotiBot(channel="noti_test", sender="Jin")
    await bot.send_to_slack_async("example message")


if __name__ == "__main__":
    import asyncio

    main()
    asyncio.run(async_main())
```