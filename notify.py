class Notify:
    def __init__(self):
        pass

    def send(self, title, msg):
        msg = "[%s] %s" % (title, msg)
        print("Notify:", msg)
        return True


class NotifyTgBot(Notify):
    def __init__(self, token, chat_id, proxy=None):
        """
        :param token: Telegram bot api token
        :param proxy: proxy creds for http and https
        Examples:
        'socks5://user:pass@host:port'
        'http://host:port'
        """
        super().__init__()
        self.chat_id = chat_id

        import telebot
        if proxy is not None:
            telebot.apihelper.proxy = {'http': proxy, 'https': proxy}
        self.bot = telebot.TeleBot(token, threaded=False)

    def send(self, title, msg):
        try:
            msg = "*%s*\n%s" % (title, msg)
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
