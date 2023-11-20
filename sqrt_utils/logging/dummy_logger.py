class DummyLogger:
    def __init__(self, print_msg=True):
        self.print_msg = print_msg

    def debug(self, msg):
        if self.print_msg:
            print(msg)

    def info(self, msg):
        if self.print_msg:
            print(msg)

    def warning(self, msg):
        if self.print_msg:
            print(msg)

    def error(self, msg):
        if self.print_msg:
            print(msg)


class DummySlackBot:
    def send_to_slack(self, msg):
        pass
