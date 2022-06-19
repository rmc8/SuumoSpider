import time

import requests as r
from bs4 import BeautifulSoup
from pandas import DataFrame, read_html, concat


class Suumo:
    def __init__(
            self,
            prefectures: str,
            region: str = "kanto",
    ):
        self.region: str = region
        self.prefectures: str = prefectures


class LocalGovernmentCode:
    URL: str = "https://ecitizen.jp/Sac/{:02}"
    
    def __init__(self):
        self.df = DataFrame()
    
    def get_code(self, pref_code: int):
        url: str = self.URL.format(pref_code)
        res = r.get(url)
        bs = BeautifulSoup(res.text, "lxml")
        pref: str = bs.find("h2") \
            .text \
            .replace("の市区町村コード一覧", "")
        df = read_html(res.text)[0]
        col_dict: dict = {
            "自治体コード": "gov_code",
            "団体名": "city",
            "ふりがな": "city_hiragana",
            "自治体コード(6桁)": "gov_code6",
        }
        df = df.rename(columns=col_dict)
        df["pref_code"] = "{:02}".format(pref_code)
        df["pref"] = pref
        df = df[["pref_code", "pref", "gov_code", "gov_code6", "city", "city_hiragana"]]
        self.df = concat([self.df, df])
        time.sleep(1)
    
    def output(self, path: str, **kwargs):
        self.df.to_csv(path, **kwargs)
