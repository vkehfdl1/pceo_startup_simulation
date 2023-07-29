import click
from Ceobank import ceobank
import os
from server import Server
import warnings

warnings.filterwarnings("ignore")


@click.command()
@click.option('--root_folder', default='./data', help='root folder to save data')
@click.option('--mode', default=0, help='mode - 0,1,2, 0 is pre A, 1 is after A, 2 is after B')
def main(root_folder, mode):
    individual_zip_filename = "individual.zip"
    team_zip_filename = "team.zip"
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)
    server = Server(root_folder)
    print("Downloading individual data...")
    individual_response = server.get_individual_data([i for i in range(967, 1042)])  # need to edit for your target ids
    print("Downloading team data...")
    team_response = server.get_team_data([i for i in range(117, 128)])  # need to edit for your target ids
    server.save_zipfile(individual_response, individual_zip_filename)
    server.save_zipfile(team_response, team_zip_filename)
    data = ceobank.load_from_zip(os.path.join(root_folder, individual_zip_filename),
                                 os.path.join(root_folder, team_zip_filename))
    pivot: bool = mode > 0
    include_result: bool = mode > 1
    if not pivot:
        team_filetype = '.csv'
    else:
        team_filetype = '.xlsx'

    data.check(mode)
    data.download_team_csv(os.path.join(root_folder, 'individual.csv'), pivot=pivot)
    data.download_individual_csv(os.path.join(root_folder, f'team{team_filetype}'),
                                 include_result=include_result)


if __name__ == '__main__':
    main()
