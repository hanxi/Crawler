from flask import Blueprint
from . import views

meituan = Blueprint('meituan', __name__)

meituan.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
meituan.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
meituan.add_url_rule('/search', 'search', views.search, methods=['GET'])
