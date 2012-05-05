#Block Manager
import pkgutil
import os


def initBlocks():
    pass
    f = open('Blocks/__init__.py', 'w')
    f.write("#Block package\n")

    f.write("__all__ = [")

    path = os.path.split(os.path.abspath(__file__))[0]
    path += "/Blocks/__init__.py"
    temp = ""
    for module, name, isPkg in pkgutil.walk_packages(path):
        if name.find("Blocks") == 0 and name != "Blocks" and name != "Blocks.Block":
            name = name[7:]
            temp += "\"" + name + "\", "
    temp = temp[:-2]
    f.write(temp + "]\n\n")

    for module, name, isPkg in pkgutil.walk_packages(path):
        if name.find("Blocks") == 0 and name != "Blocks" and name != "Blocks.Block":
            name = name[7:]
            f.write("from " + name + " import *\n")

    f.close()
