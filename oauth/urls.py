from django.urls import path

import oauth.views as oauth

urlpatterns = [
    path('', oauth.do_oauth, name='oauth.login'),
    path('logout/', oauth.log_out, name='oauth.logout'),
    path('callback/', oauth.callback, name='oauth.callback'),
]
