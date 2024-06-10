import execjs
import requests
from urllib.parse import quote
import random
import time
from lib.logger import logger
import subprocess
import re


import requests
import logging
from http.client import HTTPConnection  # py3

log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)

# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# print statements from `http.client.HTTPConnection` to console/stdout
HTTPConnection.debuglevel = 1

SEARCH_URL = 'https://i.waimai.meituan.com/openh5/search/globalpage'
COMMON_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    "Referer": "https://h5.waimai.meituan.com/",
}

def get_token(param_str, cookie):
    obj = execjs.compile(open('lib/js/meituan.js').read())
    token = obj.call('getRohrToken', param_str, cookie)
    logger.info("param_str:%s, token:%s", param_str, token)
    return token

def get_mtgsig(url, data):
    logger.info("get_mtgsig url:%s, data:%s", url, data)
    node_script = f'node lib/js/meituanmtgsig.js "{url}" "{data}"'
    process = subprocess.Popen(node_script, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
    logger.info("output:%s, error:%s", str(output), error)

    mtgsig = ''
    match = re.search(r'mtgsig\s+(\{.*?\})', str(output))
    if match:
        mtgsig = match.group(1)
        print(mtgsig)
    else:
        print('No match found')
    logger.info("mtgsig:%s", mtgsig)
    return mtgsig


def convert_cookies_to_dict(cookies):
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    return cookies

def pack_search_query():
    timestamp = str(time.time()).replace('.', '')[0:13]
    return f'?_={timestamp}&yodaReady=h5&csecplatform=4&csecversion=2.4.0'

def search_request(headers: dict, keyword: str, page: int) -> tuple[dict, bool]:
    logger.info(f"search_request keyword:{keyword} page:{page}")
    cookie = headers.get('cookie', '')
    get_cookies = convert_cookies_to_dict(cookie)
    openh5_uuid = get_cookies.get('openh5_uuid', '')
    uuid = get_cookies.get('uuid', '')
    quote_keyword = quote(keyword, 'utf-8')
    page_index = page - 1
    timestamp = str(time.time()).replace('.', '')[0:13]
    search_global_id = int(random.random() * 100000000)
    pre_param = f'keyword={quote_keyword}&page_index={page_index}&wm_order_channel=default&req_time={timestamp}&search_global_id={search_global_id}&wm_latitude=23132540&wm_longitude=113375247&search_latitude=23132540&search_longitude=113375247&wm_actual_latitude=23132540&wm_actual_longitude=113375247&wm_did=&gaoda_id=0&latitude=&longitude=&weien_id=0&wm_ctype=openapi&wm_dtype=openapi&app_model=0&page_size=20&show_mode=100&sort_type=0&query_type=0&wm_channel=8&wm_visitid=&entrance_id=0&ref_list_id=&wm_dversion=4.0.0&word_source=&personalized=1&rank_list_id=&category_type=0&search_cursor=0&search_source=0&wm_appversion=4.0.0&is_fix_keyword=false&product_tag_id=&search_page_type=0&sub_category_type=0&origin_guide_query=&slider_select_data=&activity_filter_codes=&dcContinerInstanceInfo=&product_card_page_index=0&utm_campaign=AwaimaiBwaimai&utm_term=40000&utm_source=8&utm_medium=openapi&wmUuidDeregistration=0&wmUserIdDeregistration=0&openh5_uuid={openh5_uuid}&uuid={uuid}'
    param_str = f'{SEARCH_URL}?{pre_param}'
    token = get_token(param_str, cookie)
    data = f'optimus_code=10&optimus_risk_level=71&{pre_param}&_token={token}'
    headers.update(COMMON_HEADERS)
    query = pack_search_query()

    url = f'{SEARCH_URL}{query}'
    headers["mtgsig"] = get_mtgsig(f'{SEARCH_URL}?_t={timestamp}', data)
    logger.info(
        f'url: {url}, request {url}, body={data}, headers={headers}')
    response = requests.post(url, data=data, headers=headers)
    logger.info(
        f'url: {url}, body: {data}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, body: {data}, request error, code: {response.status_code}, body: {response.text}')
        return {}, False

    return response.json(), True
