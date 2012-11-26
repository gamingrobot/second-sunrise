from panda3d.core import ConfigVariableString
import inspect


class Log:
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

    def __getName(self):
        retmod = "Module"
        frame, module, line, function, context, index = inspect.stack()[2]
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
            print self.__format("error", self.__getName(), message)

    def warning(self, *message):
        if self.loglevel <= 3:
            print self.__format("warning", self.__getName(), message)

    def info(self, *message):
        if self.loglevel <= 2:
            print self.__format("info", self.__getName(), message)

    def debug(self, *message):
        if self.loglevel <= 1:
            print self.__format("debug", self.__getName(), message)

    def manager(self, *message):
        if self.loglevel <= 0:
            print self.__format("manager", self.__getName(), message)
