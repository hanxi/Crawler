from .common import search_request

def request_search(keyword: str, cookie: str, page: int = 1) -> tuple[dict, bool]:
    """
    请求meituan获取搜索信息
    """
    headers = {"cookie": cookie}
    resp, succ = search_request(headers, keyword, page)
    if not succ:
        return {}, succ
    ret = resp.get('data', {}).get('module_list', [])
    return ret, True
