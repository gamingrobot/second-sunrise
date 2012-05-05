#Entity Manager
import pkgutil
import os


def initBlocks():
    pass
    f = open('Entities/__init__.py', 'w')
    f.write("#Entity package\n")

    f.write("__all__ = [")

    path = os.path.split(os.path.abspath(__file__))[0]
    path += "/Entities/__init__.py"
    temp = ""
    for module, name, isPkg in pkgutil.walk_packages(path):
        if name.find("Entities") == 0 and name != "Entities" and name != "Entities.Entity":
            name = name[9:]
            temp += "\"" + name + "\", "
    temp = temp[:-2]
    f.write(temp + "]\n\n")

    for module, name, isPkg in pkgutil.walk_packages(path):
        if name.find("Entities") == 0 and name != "Entities" and name != "Entities.Entity":
            name = name[9:]
            f.write("from " + name + " import *\n")

    f.close()