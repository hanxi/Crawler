import execjs
from urllib.parse import quote

SEARCH_URL = 'https://mobile.pinduoduo.com/proxy/api/search'
COMMON_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=1, i',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

def get_anti_content(cookie):
    pdd_obj = execjs.compile(open('lib/js/pdd.js').read())
    at = pdd_obj.call('getAntiContent', COMMON_HEADERS["User-Agent"], cookie)
    print(at)
    return at

def convert_cookies_to_dict(cookies):
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    return cookies

def pack_search_query(cookie, keyword, page):
    get_cookies = convert_cookies_to_dict(cookie)
    pdduid = get_cookies.get('pdd_user_id', '')
    quote_keyword = quote(keyword, 'utf-8')
    anti_content = get_anti_content(cookie)
    query = f'?pdduid={pdduid}&item_ver=lzqq&coupon_price_flag=1&source=search&search_met=qc&requery=1&list_id=xqzluqhgkl&sort=default&filter=&q={quote_keyword}&page={page}&is_new_query=1&size=50&anti_content={anti_content}'
    #&flip=0%3B0%3B0%3B0%3Bfb0ca8c3-9e03-77b3-2d95-185fb16e904e%3B%2F20%3B0%3B0%3B1c3e9579050a33272bf76579e7dd6d97
    return query

