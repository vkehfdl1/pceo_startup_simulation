import click

@click.command()
@click.option('--mode', default=0, help='mode - 0,1,2, 0 is pre A, 1 is after A, 2 is after B')
def main(mode):
    pivot: bool = mode > 0


if __name__=='__main__':
    main()

