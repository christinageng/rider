from rider.commands.base import Command


class CleanCommand(Command):
    name = "clean"
    usage = """%prog """
    summary = "clean the current cluster environment"

    def __init__(self):
        super(CleanCommand, self).__init__()

    def run(self, args):
        pass