class Chunks:
    """Chunks class manages the creation and deletion of chunks"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        meshgen = xml.find('mesh')
        if meshgen != None:
            print "DEBUG: " + meshgen.get('plugin')
            self.track = manager.get(meshgen.get('plugin')).getGenType()
        else:
            self.track = None
        print "DEBUG: " + self.track

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass
