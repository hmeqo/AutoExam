import random
import time
from datetime import datetime
from typing import Any, Tuple, Dict
from urllib.parse import parse_qs

from fastapi import Request
import requests
import numpy as np

from src.settings import BASE_DIR
from src.models import Exam


def fetch(url: str, kwds: dict):
    return url, parse_qs(kwds['body'])


def parse_fetch() -> Tuple[str, Dict[str, Any]]:
    code = (BASE_DIR / 'data' / 'fetch').read_text('UTF-8').rstrip(';')
    url, data = eval(code)
    return url, data


submit_url, fetch_data = parse_fetch()
problems = list(zip(fetch_data['submit'][0].split(','),
                    fetch_data['answer'][0].split(',')))
course_id: int = fetch_data['courseId'][0]


def random_problems(cfg: Exam):
    lst = problems.copy()
    random.shuffle(lst)
    correct_rate = cfg.request.correct_rate
    if cfg.normal_distribution.enabled:
        correct_rate = np.random.normal(
            correct_rate, cfg.normal_distribution.correct_rate_scale)
    correct_count = round(min(max(correct_rate, 0), 1) * len(lst))
    error_count = len(lst) - correct_count
    # print(correct_count, error_count)
    # print(f'正确率: {1-error_count/len(lst):.1%}', end=' ')
    for i in range(error_count):
        while True:
            o_answer = lst[i][1]
            answer = ''.join(random.choices('ABCD', k=len(o_answer)))
            if o_answer != answer:
                lst[i] = (lst[i][0], answer)
                break
    random.shuffle(lst)
    lst = [','.join(i) for i in map(list, zip(*lst))]
    return lst[0], lst[1]


def request_exam(request: Request, cfg: Exam):
    submit, answer = random_problems(cfg)
    answer_time = cfg.request.answer_time
    if cfg.normal_distribution.enabled:
        answer_time = np.random.normal(
            answer_time, cfg.normal_distribution.correct_rate_scale)
    answer_time = round(max(answer_time, 0), 2)

    data = {
        'submit': [submit],
        'answer': [answer],
        'time': [answer_time],
        'courseId': [course_id],
    }
    # return ''
    url = f'https://www.fzhd.fuzhouhuada.com:81/examTest/examination?courseId={course_id}&typesOf=1'
    headers = {
        'User-Agent': request.headers['User-Agent']
    }
    cookies = {
        'SESSION': cfg.cookies.session
    }
    requests.get(url=url, headers=headers, cookies=cookies)
    time.sleep(
        answer_time if cfg.request.consistent_time else cfg.request.submit_interval)
    return requests.post(url=submit_url, data=data, cookies=cookies).text


def main(request: Request, cfg: Exam):
    t = datetime.now()
    count = cfg.request.count
    result = ''
    for i in range(1, count + 1):
        # print(f'{i}: ', end='', flush=True)
        result += f'{i}: '
        try:
            response = request_exam(request, cfg)
        except Exception as exc:
            # print(exc, flush=True)
            result += f'{exc}\n'
            pass
        else:
            # print(response, flush=True)
            result += f'{response}\n'
            pass
        if i != count:
            time.sleep(cfg.request.interval)
    # print(f'总耗时: {datetime.now() - t}')
    result += f'总耗时: {datetime.now() - t}\n'
    return result
