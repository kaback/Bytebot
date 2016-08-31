# -*- coding: utf-8 -*-

from irc3.plugins.command import command

from bytebot_config import BYTEBOT_PLUGIN_CONFIG
from irc3 import asyncio
import json
import aiohttp

@command(permission="view")
@asyncio.coroutine
def weather(bot, mask, target, args):
    """Show the current weather for a city

        %%weather [<city>]...
    """
    config = BYTEBOT_PLUGIN_CONFIG['weather']

    if '<city>' not in args or len(args['<city>']) < 1:
        location = config['location']
    else:
        location = " ".join(args['<city>'])

    bot.log.info('Fetching weather info for %s' % location)

    url = config['url'] + location + '&appid=%s' % config['api_key']
    with aiohttp.Timeout(10):
        with aiohttp.ClientSession(loop=bot.loop) as session:
            resp = yield from aiohttp.get(url)
            if resp.status != 200:
                bot.privmsg(target, "Error while retrieving weather data")
                raise Exception()
            r = yield from resp.read()

    try:
        j = json.loads(r.decode('utf-8'))
        temp = j["main"]["temp"]
        location = "%s,%s" % (j["name"],
                              j["sys"]["country"])
    except KeyError:
        bot.privmsg(target, "Error while retrieving weather data")
        raise Exception()

    return "It's %2.2f °C in %s" % (temp, location)