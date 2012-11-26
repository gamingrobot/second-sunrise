from panda3d.core import ConfigVariableString

import inspect


class Log:
    #todo check prc log level and dont call those stacktraces
    def __init__(self):
        loglevel = ConfigVariableString('log-level', 'info').getValue()
        if loglevel == "error":
            self.loglevel = 4
        elif loglevel == "warning":
            self.loglevel = 3
        elif loglevel == "info":
            self.loglevel = 2
        elif loglevel == "debug":
            self.loglevel = 1
        elif loglevel == "manager":
            self.loglevel = 0
        self.debug("Level", loglevel)

    def __getName(self, frame, module):
        retmod = "Module"
        try:
            self_argument = frame.f_code.co_varnames[0]  # this should be self
            instance = frame.f_locals[self_argument]
            retmod = instance.__class__.__name__
        except IndexError:
            retmod = inspect.getmodulename(module)
        return retmod

    def __combine(self, message):
        return " ".join(map(str, message))

    def __format(self, level, name, message):
        if level == "info" or level == "manager":
            return "|" + name + "| " + self.__combine(message)
        else:
            return "|" + name + "(" + level + ")| " + self.__combine(message)

    #message levels
    def error(self, *message):
        if self.loglevel <= 4:
            frame, module, line, function, context, index = inspect.stack()[1]
            name = self.__getName(frame, module)
            print self.__format("error", name, message)

    def warning(self, *message):
        if self.loglevel <= 3:
            frame, module, line, function, context, index = inspect.stack()[1]
            name = self.__getName(frame, module)
            print self.__format("warning", name, message)

    def info(self, *message):
        if self.loglevel <= 2:
            frame, module, line, function, context, index = inspect.stack()[1]
            name = self.__getName(frame, module)
            print self.__format("info", name, message)

    def debug(self, *message):
        if self.loglevel <= 1:
            frame, module, line, function, context, index = inspect.stack()[1]
            name = self.__getName(frame, module)
            print self.__format("debug", name, message)

    def manager(self, *message):
        if self.loglevel <= 0:
            frame, module, line, function, context, index = inspect.stack()[1]
            name = self.__getName(frame, module)
            print self.__format("manager", name, message)
