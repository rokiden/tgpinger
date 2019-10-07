from notify import *
from socket import socket
from time import time
from config import Config
import argparse
import os


def check_tcp(host, port):
    try:
        s = socket()
        s.connect((host, port))
        s.close()
        return True
    except Exception as e:
        print(repr(e))
        return False


def create_template(path):
    try:
        os.unlink(path)
    except:
        pass
    conf = Config(path)
    conf['token'] = 'tg_api_token'
    conf['chat'] = 'chat_id'
    conf['proxy'] = None
    conf['msg_title'] = 'TgPinger'
    conf['period'] = 60 * 3
    conf['targets'] = [{'type': 'tcp', 'host': 'ya.ru', 'port': 80}, {'type': 'tcp', 'host': 'goo.gl', 'port': 443}]
    conf.save()


def work(path, debug=False):
    conf = Config(path)
    if debug:
        print(conf.tree())
        n = Notify()
    else:
        n = NotifyTgBot(conf['token'], conf['chat'], conf['proxy'])

    if 'last' not in conf:
        conf['last'] = {}
    for t in conf['targets']:
        if t['type'] == 'tcp':
            target_name = "%s:%s:%d" % (t['type'], t['host'], t['port'])
            state = check_tcp(t['host'], t['port'])
            msg = "%s %s" % (target_name, 'alive' if state else 'died')

            if target_name not in conf['last']:
                conf['last'][target_name] = {}
                n.send(conf['msg_title'], msg)
            elif time() - conf['last'][target_name]['time'] > conf['period'] * 3:
                n.send(conf['msg_title'], "Period exceeded!\n" + msg)
            elif state != conf['last'][target_name]['state']:
                n.send(conf['msg_title'], msg)

            conf['last'][target_name]['state'] = state
            conf['last'][target_name]['time'] = time()
        else:
            print('unknown target type:', t['type'])
    conf.save()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--template", help="create config template and exit")
    argparser.add_argument("--config", help="config file")
    argparser.add_argument("--debug", help="local debug mode", action="store_true")
    args = argparser.parse_args()

    if args.template is not None:
        create_template(args.template)
        print("Template config created:", args.template)
    elif args.config is not None:
        work(args.config, args.debug)
    else:
        raise Exception("Config file not specified")
