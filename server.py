import requests
from typing import List
from dotenv import load_dotenv
import os
import json

from requests import Response


class Server:
    def __init__(self, save_dir: str):
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        self.save_dir = save_dir
        self.base_url = "http://ec2-52-78-50-223.ap-northeast-2.compute.amazonaws.com"
        self.individual_url = f"{self.base_url}/api/personalbook/download"
        self.team_url = f"{self.base_url}/api/teambook/download"
        load_dotenv()
        self.bearer_token = os.getenv("BEARER_TOKEN")
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.bearer_token}'
        }

    def get_individual_data(self, ids: List[int]):
        payload = json.dumps({"id": ids})
        result = requests.post(self.individual_url, data=payload, headers=self.headers)
        result.raise_for_status()
        return result

    def get_team_data(self, ids: List[int]):
        payload = json.dumps({"id": ids})
        result = requests.post(self.team_url, data=payload, headers=self.headers)
        result.raise_for_status()
        return result

    def save_zipfile(self, response: Response, filename: str):
        if not filename.endswith(".zip"):
            raise ValueError("filename must be end with .zip")

        file_url = response.json()["url"]
        result = requests.get(f'{self.base_url}{file_url}')
        result.raise_for_status()

        with open(os.path.join(self.save_dir, filename), 'wb') as f:
            for chunk in result.iter_content(chunk_size=1024):
                f.write(chunk)


if __name__=="__main__":
    server = Server('./data/day2/')
    individual_result = server.get_individual_data([i for i in range(967, 1042)])
    team_result = server.get_team_data([i for i in range(117, 128)])
    server.save_zipfile(individual_result, "day2_individual.zip")
    server.save_zipfile(team_result, "day2_team.zip")
