import random
import time
from datetime import datetime

import requests

from config import cfg, parse_fetch

submit_url, fetch_data = parse_fetch()
problems = list(zip(fetch_data['submit'][0].split(','),
                    fetch_data['answer'][0].split(',')))
course_id: int = fetch_data['courseId'][0]
cookies = cfg.cookies
headers = cfg.headers


def random_problems():
    lst = problems.copy()
    random.shuffle(lst)
    correct_count = round(cfg.correct_rate * len(lst))
    error_count = len(lst) - correct_count
    # print(correct_count, error_count)
    print(f'正确率: {1-error_count/len(lst):.1%}', end=' ')
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


def request_exam():
    submit, answer = random_problems()
    answer_time = cfg.answer_time
    data = {
        'submit': [submit],
        'answer': [answer],
        'time': [answer_time],
        'courseId': [course_id],
    }
    # return ''
    url = f'https://www.fzhd.fuzhouhuada.com:81/examTest/examination?courseId={course_id}&typesOf=1'
    requests.get(url=url, headers=headers, cookies=cookies)
    time.sleep(answer_time if cfg.consistent_time else cfg.submit_interval)
    return requests.post(url=submit_url, data=data, cookies=cookies).text


def main():
    t = datetime.now()
    count = cfg.count
    for i in range(1, count + 1):
        print(f'{i}: ', end='', flush=True)
        try:
            response = request_exam()
        except Exception as exc:
            print(exc, flush=True)
        else:
            print(response, flush=True)
        if i != count:
            time.sleep(cfg.interval)
    print(f'总耗时: {datetime.now() - t}')


if __name__ == '__main__':
    main()
