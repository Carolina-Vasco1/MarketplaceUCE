class EventBus:
    """Simple EventBus placeholder."""
    def publish(self, event):
        raise NotImplementedError


class Logger:
    """Simple Logger placeholder."""
    def info(self, msg: str):
        raise NotImplementedError


class Tracer:
    """Simple Tracer placeholder."""
    def start_span(self, name: str):
        raise NotImplementedError


class HttpClient:
    """Simple HTTP client placeholder."""
    def request(self, method: str, url: str, **kwargs):
        raise NotImplementedError
