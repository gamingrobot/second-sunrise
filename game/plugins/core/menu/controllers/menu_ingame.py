class menu_ingame:
    """ingame menu"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        self.manager = manager

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def exit(self):
        self.manager.end()
