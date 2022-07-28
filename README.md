# PCEO Ceo Bank Web Service Extension

## Overview
포스텍 영재기업인교육원 경영시뮬레이션 진행에 있어 [씨오뱅크](adminbank.pceo.club)과 함께 이용할 수 있는 python extension입니다. 웹사이트에서 다운로드 받은 자료들을 바탕으로, 개인 및 팀 회계 장부를 하나로 합치고, 여러 오류를 자동으로 검사합니다. 

## Installation
이 git 저장소를 clone하여 python3 환경에서 import하여 사용하세요. pandas, numpy, tqdm이 필요합니다.

## Usage
먼저 씨오뱅크에서 다운로드받은 팀 회계장부 및 개인 회계장부 zip 파일을 각기 다른 경로에 압축을 풀어줍니다. 

``` python
from Ceobank import ceobank
data = ceobank('individual_path', 'team_path')
```
'individual_path'에는 개인 회계장부 엑셀 파일들이, 'team_path'에는 팀 회계장부 엑셀 파일들이 들어있어야 합니다. 

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
