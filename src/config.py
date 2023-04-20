import configparser
import random
from typing import Any
from urllib.parse import parse_qs

import numpy as np


def cfg_randfloat(section: str, option: str) -> float:
    t = config.get(section, option)
    if t.replace('.', '', 1).isdecimal():
        return float(t)
    return random.uniform(*tuple(map(float, eval(t))))


def cfg_randint(section: str, option: str) -> int:
    n = config.get(section, option)
    if n.isdecimal():
        return int(n)
    return random.randint(*tuple(map(int, eval(n))))


def fetch(url: str, kwds: dict):
    return url, parse_qs(kwds['body'])


def parse_fetch() -> tuple[str, dict[str, Any]]:
    code = open('fetch', 'r', encoding='UTF-8').read().rstrip(';')
    url, data = eval(code)
    return url, data


class Cfg:

    @property
    def count(self):
        return config.getint('request', 'count')

    @property
    def answer_time(self):
        value = cfg_randfloat('request', 'answerTime')
        if cfg.normal_enabled:
            value = np.random.normal(value, self.answer_time_scale)
        return round(max(value, 0), 2)

    @property
    def interval(self):
        return max(cfg_randfloat('request', 'interval'), 0)

    @property
    def submit_interval(self):
        return config.getfloat('request', 'submitInterval')

    @property
    def consistent_time(self):
        return config.getboolean('request', 'consistentTime')

    @property
    def answer_time_scale(self):
        return config.getfloat('normalDistribution', 'answerTimeScale')

    @property
    def correct_rate_scale(self):
        return config.getfloat('normalDistribution', 'correctRateScale')

    @property
    def correct_rate(self):
        value = cfg_randfloat('request', 'correctRate')
        if cfg.normal_enabled:
            value = np.random.normal(value, self.correct_rate_scale)
        return min(max(value, 0), 1)

    @property
    def normal_enabled(self):
        return config.getboolean('normalDistribution', 'enable')

    @property
    def headers(self) -> dict[str, Any]:
        return {
            'User-Agent': config.get('headers', 'User-Agent')
        }

    @property
    def cookies(self):
        return {
            'SESSION': config.get('cookies', 'SESSION'),
        }


config = configparser.ConfigParser()
config.read('config.ini', 'UTF-8')


cfg = Cfg()
