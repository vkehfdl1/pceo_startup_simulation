import click
from Ceobank import ceobank
import os


@click.command()
@click.option('--individual_zipfile', help='individual_zipfile')
@click.option('--team_zipfile', help='team_zipfile')
@click.option('--mode', default=0, help='mode - 0,1,2, 0 is pre A, 1 is after A, 2 is after B')
def main(individual_zipfile, team_zipfile, mode):
    data = ceobank.load_from_zip(individual_zipfile, team_zipfile)
    pivot: bool = mode > 0
    include_result: bool = mode > 1
    if not pivot:
        team_filetype = '.csv'
    else:
        team_filetype = '.xlsx'

    data.check(mode)
    data.download_team_csv(os.path.join(os.path.dirname(individual_zipfile), 'individual.csv'), pivot=pivot)
    data.download_individual_csv(os.path.join(os.path.dirname(team_zipfile), f'team{team_filetype}'),
                                 include_result=include_result)


if __name__ == '__main__':
    main()
