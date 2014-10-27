from rider.commands.build import BuildCommand

commands = {
    BuildCommand.name: BuildCommand
}


def get_summaries(ignore_hidden=True, ordered=True):
    """Yields sorted (command name, command summary) tuples."""

    cmd_items = commands.items()
    for name, command_class in cmd_items:
        if ignore_hidden and command_class.hidden:
            continue
        yield (name, command_class.summary)