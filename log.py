import time

class Color:    
    bold = '\033[1m{}\033[0m'
    fade = '\033[2m{}\033[0m'
    italic = '\033[3m{}\033[0m'
    underscore = '\033[4m{}\033[0m'
    block = '\033[7m\033{}[0m'
    strikethrough = '\033[9m{}\033[0m'
    red = '\033[91m{}\033[0m'
    green = '\033[92m{}\033[0m'
    yellow = '\033[93m{}\033[0m'
    blue = '\033[94m{}\033[0m'
    purple = '\033[95m{}\033[0m'
    aquamarine = '\033[96m{}\033[0m'
class Log:
    def __init__(self, name = "info"):
        level = {
            "debug": 0,
            "info": 1,
            "warning": 2,
            "error": 3
        }
        self.level = level[name]
    def debug(self, text):
        if self.level >= 1: return
        print Color.bold.format("[ {} ] ".format(time.strftime('%Y/%m/%d %H:%M:%S'))) + Color.green.format(text)
    def info(self, text):
        if self.level >= 2: return
        print Color.bold.format("[ {} ] ".format(time.strftime('%Y/%m/%d %H:%M:%S'))) + Color.aquamarine.format(text)
    def warning(self, text):
        if self.level >= 3: return
        print Color.bold.format("[ {} ] ".format(time.strftime('%Y/%m/%d %H:%M:%S'))) + Color.yellow.format(text)
    def error(self, text):
        print Color.bold.format("[ {} ] ".format(time.strftime('%Y/%m/%d %H:%M:%S'))) + Color.red.format(text)
