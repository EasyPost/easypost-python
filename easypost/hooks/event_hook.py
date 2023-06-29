class EventHook:
    """The parent event that occurs when a hook is triggered."""

    def __init__(self):
        self._event_handlers = []

    def __iadd__(self, handler):
        self._event_handlers.append(handler)
        return self

    def __isub__(self, handler):
        self._event_handlers.remove(handler)
        return self

    def __call__(self, *args, **kwargs):
        for event_handler in self._event_handlers:
            event_handler(*args, **kwargs)
