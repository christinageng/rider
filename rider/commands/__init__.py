from rider.commands.build import BuildCommand
from rider.commands.clean import CleanCommand
from rider.commands.provision import ProvisionCommand
from rider.commands.info import InfoCommand
from rider.commands.scale import ScaleCommand
from rider.commands.create import CreateCommand

commands = {
    BuildCommand.name: BuildCommand,
    CleanCommand.name: CleanCommand,
    ProvisionCommand.name: ProvisionCommand,
    InfoCommand.name: InfoCommand,
    ScaleCommand.name: ScaleCommand,
    CreateCommand.name: CreateCommand
}


def get_summaries(ignore_hidden=True, ordered=True):
    """Yields sorted (command name, command summary) tuples."""

    cmd_items = commands.items()
    for name, command_class in cmd_items:
        if ignore_hidden and command_class.hidden:
            continue
        yield (name, command_class.summary)