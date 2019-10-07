class Notify:
    def __init__(self):
        pass

    def send(self, title, msg):
        msg = "[%s] %s" % (title, msg)
        print("Notify:", msg)
        return True


class NotifyTgBot(Notify):
    def __init__(self, token, chat_id, proxy=None, timeout=3, max_len=-1):
        """
        :param token: Telegram bot api token
        :param proxy: proxy creds for http and https
        Examples:
        'socks5://user:pass@host:port'
        'http://host:port'
        """
        super().__init__()
        self.chat_id = chat_id
        self.timeout = timeout
        self.max_len = max_len

        import telebot
        if proxy is not None:
            telebot.apihelper.proxy = {'http': proxy, 'https': proxy}
        # import logging
        # telebot.logger.setLevel(logging.DEBUG)
        self.bot = telebot.TeleBot(token, threaded=False)

    def send(self, title, msg):
        try:
            if self.max_len > 0 and len(msg) > self.max_len:
                msg = msg[:self.max_len] + "\n..."
            msg = "*[ %s ]*\n%s" % (title, msg)
            resp = self.bot.send_message(self.chat_id, msg, parse_mode='Markdown')
            # print(resp)
            return True
        except Exception as e:
            print(repr(e))
            return False


if __name__ == '__main__':
    # n = NotifyTgBot("token", 0, 'socks5://proxy:port')
    n = Notify()
    n.send('Title', 'Test')
