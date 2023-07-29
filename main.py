import click
from Ceobank import ceobank
import os
from server import Server
import warnings

warnings.filterwarnings("ignore")


@click.command()
@click.option('--root_folder', default='./data', help='root folder to save data')
@click.option('--mode', default=1, help='mode - 0,1,2, 0 is pre A, 1 is after A, 2 is after B')
def main(root_folder, mode):
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    data = ceobank.load_from_server()
    pivot: bool = mode > 0
    include_result: bool = mode > 1
    if not pivot:
        team_filetype = '.csv'
    else:
        team_filetype = '.xlsx'

    data.check(mode)
    data.download_team_csv(os.path.join(root_folder, f'team{team_filetype}'), pivot=pivot)
    data.download_individual_csv(os.path.join(root_folder, 'individual.csv'),
                                 include_result=include_result)

    print("Done!")


if __name__ == '__main__':
    main()
