from framework.context import Context


class App:

    def __init__(self, context: Context):
        self._context = context

    def run(self):
        self._context.run_context()
        ...
