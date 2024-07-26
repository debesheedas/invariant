from dataclasses import dataclass

class AccessDenied:
    pass

class PolicyViolation(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.kwargs = kwargs
        self.ranges = kwargs.get("ranges", [])

    def __str__(self):
        kvs = ", ".join([f"{k}={v}" if k != 'ranges' else f'ranges=[<{len(v)} ranges>]' for k, v in self.kwargs.items()])
        if len(kvs) > 0: kvs = ", " + kvs
        return f"{type(self).__name__}({' '.join([str(a) for a in self.args])}{kvs})"
    
    def __repr__(self):
        return str(self)

@dataclass
class UpdateMessage(Exception):
    msg: dict
    content: str
    mode: str = "a" # p = prepend, a = append, replace = replace
    
class UpdateMessageHandler:
    def __init__(self, update_message: UpdateMessage):
        self.update_message = update_message

    def apply(self, msg: dict):
        if self.update_message.mode == "a":
            msg["content"] += self.update_message.content
        elif self.update_message.mode == "p":
            msg["content"] = self.update_message.content + msg["content"]
        elif self.update_message.mode == "r":
            msg["content"] = self.update_message.content
        return msg