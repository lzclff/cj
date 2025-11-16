import json
import logging
import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from wxcloudrun.models import Counters


logger = logging.getLogger('log')


def index(request):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def get_wechat_auth_url(request):
    """
    获取微信授权URL
    支持两种格式：
    1. 标准格式：{"redirect_uri": "xxx", "state": "xxx", "scope": "xxx"}
    2. 云托管格式：{"config": {...}, "data": {...}}
    """
    try:
        # 解析请求数据
        if request.method == 'POST':
            try:
                request_data = json.loads(request.body)
            except:
                return JsonResponse({
                    'errcode': 40001,
                    'errmsg': '无效的JSON数据'
                })
        else:
            request_data = request.GET.dict()
        
        logger.info(f"获取授权URL请求数据: {request_data}")
        
        # 检查是否为云托管格式
        if 'config' in request_data and 'data' in request_data:
            # 云托管格式
            data = request_data.get('data', {})
        else:
            # 标准格式
            data = request_data
        
        # 获取参数
        redirect_uri = data.get('redirect_uri', 'http://127.0.0.1:8082/wechat/callback')
        state = data.get('state', 'default_state')
        scope = data.get('scope', 'snsapi_userinfo')
        
        # 构建微信授权URL
        auth_url = (
            f"https://open.weixin.qq.com/connect/oauth2/authorize?"
            f"appid={settings.WECHAT_APPID}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
            f"&state={state}#wechat_redirect"
        )
        
        logger.info(f"生成的授权URL: {auth_url}")
        
        return JsonResponse({
            'errcode': 0,
            'errmsg': 'success',
            'auth_url': auth_url
        })
        
    except Exception as e:
        logger.error(f"获取授权URL失败: {e}")
        return JsonResponse({
            'errcode': 50001,
            'errmsg': f'服务器错误: {str(e)}'
        })


@csrf_exempt
def get_wechat_user_info(request):
    """
    获取微信用户信息
    支持两种格式：
    1. 标准格式：{"code": "xxx", "state": "xxx"}
    2. 云托管格式：{"config": {...}, "data": {...}}
    """
    try:
        # 解析请求数据
        if request.method == 'POST':
            try:
                request_data = json.loads(request.body)
            except:
                return JsonResponse({
                    'errcode': 40001,
                    'errmsg': '无效的JSON数据'
                })
        else:
            request_data = request.GET.dict()
        
        logger.info(f"获取用户信息请求数据: {request_data}")
        
        # 检查是否为云托管格式
        if 'config' in request_data and 'data' in request_data:
            # 云托管格式
            data = request_data.get('data', {})
        else:
            # 标准格式
            data = request_data
        
        # 获取参数
        code = data.get('code')
        state = data.get('state', '')
        
        if not code:
            return JsonResponse({
                'errcode': 40002,
                'errmsg': '缺少授权码code'
            })
        
        # 获取access_token
        token_url = (
            f"https://api.weixin.qq.com/sns/oauth2/access_token?"
            f"appid={settings.WECHAT_APPID}"
            f"&secret={settings.WECHAT_APPSECRET}"
            f"&code={code}"
            f"&grant_type=authorization_code"
        )
        
        logger.info(f"请求access_token: {token_url}")
        
        token_response = requests.get(token_url, timeout=10)
        token_data = token_response.json()
        
        if 'errcode' in token_data and token_data['errcode'] != 0:
            return JsonResponse({
                'errcode': token_data['errcode'],
                'errmsg': token_data.get('errmsg', '获取access_token失败')
            })
        
        access_token = token_data.get('access_token')
        openid = token_data.get('openid')
        
        if not access_token or not openid:
            return JsonResponse({
                'errcode': 50002,
                'errmsg': '获取access_token失败'
            })
        
        # 获取用户信息
        userinfo_url = (
            f"https://api.weixin.qq.com/sns/userinfo?"
            f"access_token={access_token}"
            f"&openid={openid}"
            f"&lang=zh_CN"
        )
        
        userinfo_response = requests.get(userinfo_url, timeout=10)
        userinfo_data = userinfo_response.json()
        
        if 'errcode' in userinfo_data and userinfo_data['errcode'] != 0:
            return JsonResponse({
                'errcode': userinfo_data['errcode'],
                'errmsg': userinfo_data.get('errmsg', '获取用户信息失败')
            })
        
        # 构建用户信息
        user_info = {
            'openid': userinfo_data.get('openid'),
            'nickname': userinfo_data.get('nickname'),
            'sex': userinfo_data.get('sex'),
            'province': userinfo_data.get('province'),
            'city': userinfo_data.get('city'),
            'country': userinfo_data.get('country'),
            'headimgurl': userinfo_data.get('headimgurl'),
            'privilege': userinfo_data.get('privilege', []),
            'unionid': userinfo_data.get('unionid', ''),
        }
        
        logger.info(f"获取用户信息成功: {user_info}")
        
        return JsonResponse({
            'errcode': 0,
            'errmsg': 'success',
            'user_info': user_info
        })
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return JsonResponse({
            'errcode': 50001,
            'errmsg': f'服务器错误: {str(e)}'
        })
