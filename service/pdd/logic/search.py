from .common import SEARCH_URL, COMMON_HEADERS, pack_search_query
import requests
import json
import re
from lib.logger import logger
from urllib.parse import quote

def request_search(keyword: str, cookie: str, page: int = 1) -> tuple[dict, bool]:
    """
    请求pdd获取搜索信息
    """
    ret = []
    query = pack_search_query(cookie, keyword, page)
    url = f'{SEARCH_URL}{query}'
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    try:
        logger.info(f'url: {url}')
        with requests.get(url, headers=headers) as res:
            res = json.loads(res.text)
            ret = res["items"]
            ret_count = len(ret)
            logger.info(f'ret_count: {ret_count}')
    except Exception as e:
        print(e)
        return {}, False

    return ret, True
