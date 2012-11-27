class Events:
    """Events System"""
    def __init__(self):
        self.events = {}

    def hookEvent(self, eventName, callback):
        if not (eventName in self.events):
            self.events[eventName] = []
        self.events[eventName].append(callback)

    def unHookEvent(self, eventName, callback):
        pass

    def triggerEvent(self, eventName, data):
        if eventName in self.events:
            for callback in self.events[eventName]:
                callback(data)
