# PCEO Ceo Bank Web Service Extension

## Overview
포스텍 영재기업인교육원 경영시뮬레이션 진행에 있어 [씨오뱅크](adminbank.pceo.club)과 함께 이용할 수 있는 python extension입니다. 웹사이트에서 다운로드 받은 자료들을 바탕으로, 개인 및 팀 회계 장부를 하나로 합치고, 여러 오류를 자동으로 검사합니다. 

## Installation
이 git 저장소를 clone하여 python3 환경에서 import하여 사용하세요. pandas, numpy, tqdm이 필요합니다.

## Environment setup

먼저 `Ceobank.py`의 `load_from_server`에서 individual 및 team id를 기수에 맞게 변경하세요.
그리고 `.env` 파일에 `BEARER_TOKEN`을 적어주세요.
해당 값을 어떻게 구하는지 모르겠으면 저한테 물어보세요.

## QuickStart
``` shell
python main.py --mode={mode} --root_folder={root_folder}
```

위 코드를 터미널에서 실행하면 로드, 체크, 결과 파일 저장까지 root_folder 경로에 할 수 있습니다.


## Usage
먼저 씨오뱅크에서 다운로드받은 팀 회계장부 및 개인 회계장부 zip 파일의 경로를 파일까지 아래 코드에 입력합니다.

``` python
from Ceobank import ceobank
data = ceobank.load_from_zip('개인 회계장부 zip 파일 경로', '팀 회계장부 zip 파일 경로')
```

아래 코드를 실행하면 서버에서 직접 다운로드 받을 수 있습니다.
단, 이 경우 .env 파일에 Bearer Token과 타겟하는 id를 입력해야 합니다.
크롬의 개발자 모드 네트워크 탭을 실행시켜 놓은 상태로, 다운로드 버튼을 클릭하면 Request Headers에 Bearer Token이 있습니다.
또한, Payload 탭에서 클릭한 id list를 확인할 수 있습니다.

``` python
from Ceobank import ceobank
data = ceobank.load_from_server(individual_start_id='개인 회계장부 시작 id', team_start_id='팀 회계장부 시작 id', individual_end_id='개인 회계장부 끝 id', team_end_id='팀 회계장부 끝 id')
```

---

``` python
data.download_team_csv('저장 경로 및 파일 이름')
```
위 코드로 팀 파일을 저장합니다. 파일 확장자 명은 반드시 pivot이 True일 경우 .xlsx, 아닐 경우 .csv입니다. (pivot을 선택할 경우 더욱 정리된 형태로 다운로드 받을 수 있습니다)

``` python
data.download_individual_csv('저장 경로 및 파일 이름')
```
위 코드로 개인 파일을 저장합니다. 파일 확장자 명은 반드시 .csv이어야 합니다. include_result 파라미터를 False로 설정하면 개인 투자 결과를 보지 않을 수 있습니다. 

``` python
data.check(mode=mode)
```
위 코드로 오류를 검사합니다. mode값은 1차 투자 이전에 0, 1차 투자 이후 1, 2차 투자 이후에는 2입니다. 
1차 투자금 및 2차 투자금 개인 회계 장부와 팀 회계장부 연동 오류, 개인 회계 장부 마이너스 오류, 일정 기업 투자 한도 초과 오류, 팀 회계장부 잔액 오류를 검사할 수 있습니다. 

``` python
data.get_team_credit()
```
위 코드로 각 팀의 평균 크레딧을 열람하여 대출에 참고할 수 있습니다. 

## Contacts
질문 사항 및 오류는 자유롭게 연락주세요. 
