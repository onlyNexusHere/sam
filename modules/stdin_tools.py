
from .SamModule import SamModule


class StdinTools(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    def __init__(self, sam=None):
        super().__init__("StdinTools", SamControl=sam)

    def run(self):
        pass
