from direct.directnotify.DirectNotify import DirectNotify
import inspect


class Log:
    #todo check prc log level and dont call those stacktraces
    def __init__(self):
        pass

    def getCat(self, mod):
        return DirectNotify().newCategory(mod)

    def getName(self, frame, module):
        retmod = "Module"
        try:
            self_argument = frame.f_code.co_varnames[0]  # this should be self
            instance = frame.f_locals[self_argument]
            retmod = instance.__class__.__name__
        except IndexError:
            retmod = inspect.getmodulename(module)
        return retmod

    def combine(self, message):
        return " ".join(map(str, message))

    def error(self, *message):
        frame, module, line, function, context, index = inspect.stack()[1]
        self.getCat(self.getName(frame, module)).error(self.combine(message))

    def warning(self, *message):
        frame, module, line, function, context, index = inspect.stack()[1]
        self.getCat(self.getName(frame, module)).warning(self.combine(message))

    def info(self, *message):
        frame, module, line, function, context, index = inspect.stack()[1]
        self.getCat(self.getName(frame, module)).info(self.combine(message))

    def debug(self, *message):
        frame, module, line, function, context, index = inspect.stack()[1]
        self.getCat(self.getName(frame, module)).debug(self.combine(message))
