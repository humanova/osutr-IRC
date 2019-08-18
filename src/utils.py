import codecs
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
log_path = config['log']['path']

def get_settings():
    host = config['irc']['host']
    port = int(config['irc']['port'])
    nick = config['irc']['nick']
    password = config['irc']['password']
    channel = config['irc']['channel']
    
    return host, port, nick, password, channel

def log_msg(nick, msg):
    file = codecs.open(config['log']['path'], "a+", "utf-8")

    log_msg = f"[{nick}] {msg}"
    file.write(log_msg + "\n")
    print(log_msg)