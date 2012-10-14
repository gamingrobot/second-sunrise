class MeshGenerators:
    """MeshGenerators for the chunks"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        self.meshgentype = xml.get('gentype')
        print "DEBUG: " + self.meshgentype

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def getGenType(self):
        return self.meshgentype
