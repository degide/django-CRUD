from django.urls import path
from .views import all_accounts, \
    create_account, \
    delete_account, \
    update_account, \
    account_by_unique_id, \
    account_login, \
    verify_token

urlpatterns = [
    path('', all_accounts, name="accounts"),
    path('create', create_account, name="create"),
    path('login', account_login, name="login"),
    path('delete', delete_account, name="delete"),
    path('update', update_account, name="update"),
    path('by-id', account_by_unique_id, name="byId"),
    path('verify-token', verify_token, name="verifyToken")
]