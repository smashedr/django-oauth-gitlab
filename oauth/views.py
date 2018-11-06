import logging
import requests
import urllib.parse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from oauth.models import Oauth

logger = logging.getLogger('app')
config = settings.CONFIG


def do_oauth(request):
    """
    # View  /oauth/
    """
    oauth = Oauth.objects.all()[0]
    request.session['login_redirect_url'] = get_next_url(request)
    params = {
        'client_id': oauth.client_id,
        'redirect_uri': oauth.redirect_uri,
        'response_type': oauth.response_type,
        'scope': oauth.scope,
    }
    url_params = urllib.parse.urlencode(params)
    url = 'https://git.cssnr.com/oauth/authorize?{}'.format(url_params)
    return HttpResponseRedirect(url)


def callback(request):
    """
    # View  /oauth/callback/
    """
    try:
        oauth_code = request.GET['code']
        logger.debug('oauth_code: {}'.format(oauth_code))
        access_token = get_token(oauth_code)
        logger.debug('access_token: {}'.format(access_token))
        gitlab_profile = get_profile(access_token)
        logger.debug(gitlab_profile)
        auth = login_user(request, gitlab_profile)
        if not auth:
            err_msg = 'Unable to complete login process. Report as a Bug.'
            return HttpResponse(err_msg, content_type='text/plain')
        try:
            next_url = request.session['login_redirect_url']
        except Exception:
            next_url = '/'
        return HttpResponseRedirect(next_url)

    except Exception as error:
        logger.exception(error)
        err_msg = 'Fatal Login Error. Report as Bug: %s' % error
        return HttpResponse(err_msg, content_type='text/plain')


@require_http_methods(['POST'])
def log_out(request):
    """
    View  /oauth/logout/
    """
    next_url = get_next_url(request)
    request.session['login_next_url'] = next_url
    logout(request)
    return redirect(next_url)


def login_user(request, profile):
    """
    Login or Create New User
    """
    try:
        user = User.objects.filter(username=profile['username']).get()
        user = update_profile(user, profile)
        user.save()
        login(request, user)
        return True
    except ObjectDoesNotExist:
        user = User.objects.create_user(profile['username'], profile['email'])
        user = update_profile(user, profile)
        user.save()
        login(request, user)
        return True
    except Exception as error:
        logger.exception(error)
        return False


def get_token(code):
    """
    Post OAuth code to Twitch and Return access_token
    """
    oauth = Oauth.objects.all()[0]
    url = 'https://git.cssnr.com/oauth/token'
    data = {
        'client_id': oauth.client_id,
        'client_secret': oauth.client_secret,
        'redirect_uri': oauth.redirect_uri,
        'code': code,
        'grant_type': oauth.grant_type,
    }
    # headers = {'Accept': 'application/json'}
    r = requests.post(url, data=data, timeout=10)
    logger.debug('status_code: {}'.format(r.status_code))
    logger.debug('content: {}'.format(r.content))
    return r.json()['access_token']


def get_profile(access_token):
    """
    Get Twitch Profile for Authenticated User
    """
    url = 'https://git.cssnr.com/api/v4/user'
    params = {'access_token': access_token}
    r = requests.get(url, params=params, timeout=10)
    logger.debug('status_code: {}'.format(r.status_code))
    logger.debug('content: {}'.format(r.content))
    return r.json()


def update_profile(user, profile):
    """
    Update user_profile from GitHub data
    """
    user.first_name = profile['name']
    user.email = profile['email']
    return user


def get_next_url(request):
    """
    Determine 'next' Parameter
    """
    try:
        next_url = request.GET['next']
    except Exception:
        try:
            next_url = request.POST['next']
        except Exception:
            try:
                next_url = request.session['login_next_url']
            except Exception:
                next_url = '/'
    if not next_url:
        next_url = '/'
    return next_url
