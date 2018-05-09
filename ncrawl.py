import time
from urllib.parse import urlencode

import requests
# from pyquery import PyQuery as pq

start_id = '1739746697'

crawl_list = [start_id]
crawl_index = 0
crawl_set = set()
crawl_set.add(start_id)

all_pr_pair = []


base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/1739746697',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_page(page, val):
    params = {
        'type': 'uid',
        'value': val,
        'containerid': '107603' + val,
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json = response.json()

            if json:
                pr_pair = []
                try:
                    items = json.get('data').get('cards')
                except Exception as e:
                    print(e)
                    return pr_pair
                for item in items:
                    try:
                        mblog = item.get('mblog')
                        post = mblog.get('text')

                        rid = mblog.get('id')

                        new_url = 'https://m.weibo.cn/api/comments/show?id=' + rid + '&page=1'

                        new_res = requests.get(new_url)
                        all_data = new_res.json().get('data').get('data')
                        # print("ddd")

                        response = all_data[0].get('text')
                        pr_pair.append((post, response))

                        for data in all_data:
                            usr_id = data.get('user').get('id')
                            usr_id = str(usr_id)
                            if usr_id in crawl_set:
                                pass
                            else:
                                crawl_set.add(usr_id)
                                crawl_list.append(usr_id)
                            # print(str(usr_id))
                            # input()

                    except Exception as e:
                        # print(e)
                        pass
                return pr_pair

            # return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return []


def my_parse_json(json):
    if json:
        pr_pair = []
        try:
            items = json.get('data').get('cards')
        except Exception as e:
            print(e)
            print('the json has no crads')
            return pr_pair
        for item in items:
            try:
                mblog = item.get('mblog')
                post = mblog.get('text')

                # bid = mblog.get('bid')
                rid = mblog.get('id')

                # new_header = {
                #     'Host': 'm.weibo.cn',
                #     'Referer': 'https://m.weibo.cn/u/' + bid,
                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                #     'X-Requested-With': 'XMLHttpRequest',
                # }
                new_url = 'https://m.weibo.cn/api/comments/show?id=' + rid + '&page=1'

                # new_res = requests.get(new_url, headers=new_header)
                new_res = requests.get(new_url)
                all_data = new_res.json().get('data').get('data')
                # print("ddd")

                response = all_data[0].get('text')
                pr_pair.append((post, response))

                for data in all_data:
                    usr_id = data.get('user').get('id')
                    usr_id = str(usr_id)
                    if usr_id in crawl_set:
                        pass
                    else:
                        crawl_set.add(usr_id)
                        crawl_list.append(usr_id)
                    # print(str(usr_id))
                    # input()

            except Exception as e:
                # print(e)
                pass
        return pr_pair


# json = get_page(1, '2830678474')
# pr = my_parse_json(json)

fout = open("res.txt", 'w', encoding='utf-8')
start = time.time()
total_len = 0

while crawl_index < len(crawl_list) and crawl_index < 100000:
    # for every one, at most crawl 10 pages
    for i in range(1, 11):
        # json = get_page(i, crawl_list[crawl_index])
        # pr = my_parse_json(json)
        pr = get_page(i, crawl_list[crawl_index])
        # print(len(pr))
        try:
            for pair in pr:
                fout.write(pair[0] + '\n')
                fout.write(pair[1] + '\n')
                fout.write('\n')
            # all_pr_pair.extend(pr)
            total_len += len(pr)
        except Exception as e:
            pass
    crawl_index += 1

    if crawl_index % 1000 == 0:
        end = time.time()
        print(crawl_index, total_len, end - start)
    # print(crawl_index, len(all_pr_pair))

fout.close()
