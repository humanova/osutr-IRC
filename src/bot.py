import asyncio
from time import gmtime, strftime, time

import bottom
from utils import log_msg, get_settings

host, port, nick, password, channel = get_settings()

bot = bottom.Client(host=host, port=port, ssl=False)
loop = asyncio.get_event_loop()
loop.set_debug(True)

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    print("Connected.")
    
    bot.send('PASS', password=password)
    bot.send('NICK', nick=nick)
    bot.send('USER', user=nick, realname=nick)

    # wait till server motd
    done, pending = await asyncio.wait(
        [bot.wait("RPL_ENDOFMOTD"),
         bot.wait("ERR_NOMOTD")],
        return_when=asyncio.FIRST_COMPLETED
    )

    for future in pending:
        future.cancel()

    print("joining %s" % channel)
    bot.send('JOIN', channel=channel)

@bot.on('CLIENT_DISCONNECT')
async def reconnect(**kwargs):
    print("Reconnecting...")

    await asyncio.sleep(2)
    loop.create_task(bot.connect())
    await bot.wait("CLIENT_CONNECT")

@bot.on('PRIVMSG')
def privmsg(**kwargs):
    if kwargs["target"] == '#turkish':
        nick = kwargs["nick"]
        msg = kwargs["message"]
        log_msg(nick, msg)

if __name__ == "__main__":
    print("Connecting...")
    loop.create_task(bot.connect())
    loop.run_forever()