from config import Config
from notify import *
from argparse import ArgumentParser
from os import unlink
from sys import stdin


def create_template(path):
    try:
        unlink(path)
    except:
        pass
    conf = Config(path)
    conf['token'] = 'tg_api_token'
    conf['chat'] = 'chat_id'
    conf['proxy'] = None
    conf['msg_title'] = 'TgMail'
    conf['mail_body_len'] = 2000
    conf.save()


def parse_stdin():
    msg = {'From': '', 'Subject': '', 'Body': ''}
    in_header = False
    in_body = False
    for line in stdin:
        if in_body:
            # + (' ' if msg['Body'] else '')
            msg['Body'] = msg['Body'] + line.lstrip()
        elif in_header:
            if str(line).startswith('Subject: '):
                msg['Subject'] = line[9:].strip()
            elif line == '\n':
                in_body = True
        elif line.startswith('From '):
            msg['From'] = line[5:].strip()
            in_header = True
    return msg


def mail_repr(msg, body_len=2000):
    def escape_head(s: str):
        tags = ['*', '_', '[', '`']
        for t in tags:
            s = s.replace(t, '\\' + t)
        return s

    def escape_body(s: str):
        return s.replace('`', "'")

    if len(msg['Body']) > body_len:
        msg['Body'] = msg['Body'][:body_len] + '\n...'
    return "*From* %s\n*Subject* %s\n*Body*\n`%s`" % (
        escape_head(msg['From']), escape_head(msg['Subject']), escape_body(msg['Body']))


def work(path, debug=False):
    conf = Config(path)
    if debug:
        print(conf.tree())
        n = Notify()
    else:
        n = NotifyTgBot(conf['token'], conf['chat'], conf['proxy'])

    queue = conf['queue'] if 'queue' in conf else []
    queue.append(parse_stdin())

    while queue:
        if n.send(conf['msg_title'], mail_repr(queue[0], conf['mail_body_len'])):
            queue.pop(0)
        else:
            break

    conf['queue'] = queue

    conf.save()


if __name__ == '__main__':
    argparser = ArgumentParser()
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
