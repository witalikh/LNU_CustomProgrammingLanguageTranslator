from abc import ABC


class Usable:
    def __init__(self):
        self._usages = None

    @property
    def usages(self):
        return self._usages

    def use(self):
        if self._usages is None:
            self._usages = 1
        else:
            self._usages += 1
