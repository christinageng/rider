from rider.commands.base import Command


class StatusCommand(Command):
    name = "status"
    usage = """%prog """
    summary = "show status of the current cluster environment"

    def __init__(self):
        super(StatusCommand, self).__init__()