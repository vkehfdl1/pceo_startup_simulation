import numpy as np
import pandas as pd
from glob import glob
import os
from tqdm import tqdm


class ceobank:
    def __init__(self, individual_path, team_path):
        self.individual_file_list = sorted(glob(os.path.join(individual_path, "*.xlsx")))
        self.team_file_list = sorted(glob(os.path.join(team_path, "*.xlsx")))

    def load(self):
        team_data = []
        individual_data = []
        for filepath in tqdm(self.team_file_list):
            history, basic = self._load_team_single(filepath)
            team_data.append([history, basic])
        print("End Team Data Load")
        for filepath in tqdm(self.individual_file_list):
            history, basic = self._load_individual_single(filepath)
            individual_data.append([history, basic])
        print("End Individual Data Load")

        # Team
        team_final = pd.DataFrame([])
        for i, df in enumerate(team_data):
            temp = df[0]
            meta = df[1]
            temp.insert(loc=0, column='team_name', value=meta['team_name'])
            temp = temp.reset_index(drop=True)
            if i == 0:
                team_final = temp
            else:
                team_final = pd.concat([team_final, temp], axis=0, ignore_index=True)
        self.team_data = team_final

        self.team_list = self.team_data.team_name.unique()
        self._pivot_team_data()
        # Individual
        individual_final = pd.DataFrame([])
        for i, df in enumerate(individual_data):
            temp = df[0]
            # temp 값에서 초기투자금, 각 1차 투자금액, 2차 투자금액 입력해야함.
            init_investment = self._get_init_investment(temp)
            reward = self._get_individual_reward(temp)
            meta = df[1]
            first_investment = self._get_investment(temp, mode=1)
            second_investment = self._get_investment(temp, mode=2)
            init_value = [meta['student_name'], meta['team_name'], meta['init_ceo'], meta['init_credit'],
                          init_investment, reward]
            init_value.extend(first_investment)
            init_value.extend(second_investment)
            init_col = ['student_name', 'team_name', 'init_ceo', 'init_credit', 'init_investment', 'reward']
            first_investment_col_name = ['1st_' + s for s in self.team_list]
            second_investment_col_name = ['2nd_' + s for s in self.team_list]
            init_col.extend(first_investment_col_name)
            init_col.extend(second_investment_col_name)
            new_temp = pd.DataFrame([init_value], columns=init_col)
            if i == 0:
                individual_final = new_temp
            else:
                individual_final = pd.concat([individual_final, new_temp], axis=0, ignore_index=True)

        individual_final[
            'remain'] = individual_final.init_ceo + individual_final.reward - individual_final.init_investment - individual_final.iloc[
                                                                                                                 :,
                                                                                                                 6:34].sum(
            axis=1)
        self.individual_data = individual_final

    def get_team_credit(self):
        result = pd.DataFrame([])
        for i, team_name in enumerate(self.team_list):
            team_credit = self.individual_data.loc[lambda x: x.team_name == team_name].init_credit.mean()
            temp = pd.DataFrame([[team_name, team_credit]], columns=['team_name', 'team_credit'])
            if i == 0:
                result = temp
            else:
                result = pd.concat([result, temp], axis=0)
        return result

    def _get_individual_result(self):
        remain_list = list()
        invest_list = list()
        for team_name in self.team_list:
            one_team = self.team_data.loc[lambda x: x.team_name == team_name]
            remain_list.append(self._get_team_remain(one_team))
            invest_list.append(self._get_team_investment_total(one_team))
        df = self.individual_data.copy()
        df = df.fillna(0)
        individual_result = list()
        for i in range(len(self.individual_data)):
            individual = df.iloc[i, :]
            result = 0
            for j in range(len(self.team_list)):
                first = individual[j + 6]
                second = individual[j + 20]
                share = ((first * 1.3) + (second * 1.2)) / invest_list[j]
                result += (share * remain_list[j])
            individual_result.append(result)
        self.individual_data['result'] = individual_result
        return individual_result

    def check(self, mode):
        """
        mode - 0,1,2
        0 : preA
        1 : after series A
        2 : after sereis B
        """
        # 6:20 팀 이름에 따라 반드시 수정하세요!
        if mode >= 1:
            if (self.team_data.loc[lambda x: x.content == "1차 투자금"].income.values == self.individual_data.iloc[:,
                                                                                     6:20].sum(
                    axis=0).values).sum() == len(self.team_list):
                print("1차 투자금 개인 및 팀 연동 문제 없음")
            else:
                print("*******1차 투자금 개인 및 팀 연동 오류 발생*******")

            if (self.individual_data.iloc[:, 6:20] > 500000).sum(axis=0).sum() == 0:
                print("1차 투자 초과투자자 없음")
            else:
                print("*******1차 투자금 개인 초과 투자 오류 발생*******")

        if mode >= 2:
            if (self.team_data.loc[lambda x: x.content == "2차 투자금"].income.values == self.individual_data.iloc[:,
                                                                                     20:34].sum(
                    axis=0).values).sum() == len(self.team_list):
                print("2차 투자금 개인 및 팀 연동 문제 없음")
            else:
                print("*******2차 투자금 개인 및 팀 연동 오류 발생*******")

            df = self.individual_data.copy()
            df = df.fillna(0)
            for i in range(len(self.team_list)):
                if len((df.iloc[:, i + 6] + df.iloc[:, i + 20]).loc[lambda x: x > 500000]) != 0:
                    print("*******특정 기업 투자 상한선 초과 오류 발생*******")

        if len(self.individual_data.loc[lambda x: x.remain < 0]) == 0:
            print("개인 회계 장부 마이너스 없음")
        else:
            print("*******개인 회계 장부 마이너스 오류 발생*******")

        for name in self.team_list:
            team_data = self.team_data.loc[lambda x: x.team_name == name]
            income = team_data.loc[lambda x: x.outcome.isnull()].income.sum()
            outcome = team_data.loc[lambda x: x.income.isnull()].outcome.sum()
            remain = team_data.remain.iloc[-1]
            if income - outcome == remain:
                print("{0} 팀 회계장부 정상".format(name))
            else:
                print("*******{0} 팀 회계장부 잔액에 오류 발생*******".format(name))

    def _pivot_team_data(self):
        df = self.team_data.copy()
        df['ceo'] = df[['income', 'outcome']].max(axis=1)
        df['day'] = df['date'].map(lambda x: self._get_day(x))
        df['isincome'] = df.outcome.isna()
        df['type'] = df['isincome'].map(lambda x: 'income' if x else 'outcome')
        # self.pivot_team_data = pd.pivot_table(df, values='ceo', index=['team_name', 'type', 'content'], columns=['day'])
        self.pivot_team_data = df.groupby(['team_name', 'type', 'content', 'day'], sort=False)['ceo'].sum().unstack(
            'day')

    def download_team_csv(self, filepath, pivot=True):
        """
        params must be full filepath contains filename, must be csv filetype
        """
        if pivot:
            writer = pd.ExcelWriter(filepath)
            for manager in self.pivot_team_data.index.get_level_values(0).unique():
                temp_df = self.pivot_team_data.xs(manager, level=0)
                temp_df.to_excel(writer, manager)
            writer.save()
        else:
            result = self.team_data.copy()
            result.columns = ['팀이름', '날짜', '항목', '수입', '지출', '잔액', '기타']
            result.to_csv(filepath, index=False, encoding='utf-8-sig')
        print('save complete')

    def download_individual_csv(self, filepath, include_result=True):
        if include_result:
            self._get_individual_result()
        result = self.individual_data.copy()
        result_col = ['학생이름', '팀이름', '초기씨오', '초기크레딧', '초기자본금', '개인상금']
        investment1_col = ['1차 투자_' + s for s in self.team_list]
        investment2_col = ['2차 투자_' + s for s in self.team_list]
        result_col.extend(investment1_col)
        result_col.extend(investment2_col)
        result_col.extend(['잔액'])
        if include_result:
            result_col.extend(['최종 결과'])
        result.columns = result_col
        result.to_csv(filepath, index=False, encoding='utf-8-sig')
        print('save complete')

    def _get_day(self, datetime):
        return int((datetime.split('-')[2]).split(' ')[0]) - 18

    def _get_init_investment(self, df):
        return df.loc[lambda x: x.content == '내 팀 자본금'].outcome.sum()

    def _get_individual_reward(self, df):
        return df.loc[lambda x: (x.content == '강의 태도 우수자') | (x.content == '기업가 강연 후기 우수자') | (
                    x.content == '내배한 우수자')].income.sum() - df.loc[lambda x: x.content.str.contains('벌금')].outcome.sum()

    def _get_investment(self, df, mode):
        search_col = ""
        if mode == 1:
            search_col = "1차 투자금"
        elif mode == 2:
            search_col = "2차 투자금"
        else:
            raise ValueError("Invalid value at mode")

        result = []
        investment_data = df.loc[lambda x: x.content.str.contains(search_col)]
        for team_name in self.team_list:
            investment_value = investment_data.loc[lambda x: x.content.str.contains(team_name)].outcome.sum()
            if investment_value > 0:
                result.append(investment_value)
            else:
                result.append(np.nan)
        return result

    def _get_team_remain(self, one_team):
        return max(0, one_team.remain.iloc[-1])

    def _get_team_investment_total(self, one_team):
        investment1 = one_team.loc[lambda x: x.content == "1차 투자금"].income.sum()
        investment2 = one_team.loc[lambda x: x.content == "2차 투자금"].income.sum()
        return (investment1 * 1.3) + (investment2 * 1.2)

    def _load_team_single(self, filepath):
        df = pd.read_excel(filepath, engine='openpyxl')
        basic_dict = {
            'team_name': df.iloc[0, 2],
            'accountant_name': df.iloc[0, 4],
            'init_money': df.iloc[2, 2]
        }
        spending_history = df.iloc[5:, 1:7]
        spending_history.columns = ['date', 'content', 'income', 'outcome', 'remain', 'etc']
        spending_history = spending_history[spending_history.date.notnull()]
        return spending_history, basic_dict

    def _load_individual_single(self, filepath):
        df = pd.read_excel(filepath, engine='openpyxl')
        basic_dict = {
            'team_name': df.iloc[0, 2],
            'student_name': df.iloc[0, 4],
            'student_num': df.iloc[0, 6],
            'init_ceo': df.iloc[2, 2],
            'init_credit': df.iloc[2, 4]
        }
        spending_history = df.iloc[5:, 1:7]
        spending_history.columns = ['date', 'content', 'income', 'outcome', 'remain', 'etc']
        spending_history = spending_history[spending_history.date.notnull()]
        return spending_history, basic_dict
