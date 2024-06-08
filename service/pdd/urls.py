from flask import Blueprint
from . import views

pdd = Blueprint('pdd', __name__)

pdd.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
pdd.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
pdd.add_url_rule('/search', 'search', views.search, methods=['GET'])
