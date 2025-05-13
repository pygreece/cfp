import click

from cfp.app import assignments


@click.group()
def cfp() -> None:
    pass


cfp.add_command(assignments)


if __name__ == "__main__":
    cfp()
