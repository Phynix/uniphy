from . import handler

# TODO: singleton?
class OutputManager():
    def __init__(self):
        self.outputs = {}

    def __call__(self, name='DEFAULT_MANAGER'):
        new_out = self.outputs.get(name)
        if not new_out:
            new_out = handler.Output(name)
            self.outputs[name] = new_out

        return new_out


