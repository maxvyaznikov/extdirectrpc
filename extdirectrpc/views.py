# coding=utf-8

'''
Copyright 2012-2013

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
Модуль контроллеров Ext.Direct.RPC стека
@authors: obraztsov, Max Vyaznikov
'''

from re import escape
from rpcstack import RPC
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.defaults import url
from django.conf import settings


'''
View для удаленного вызова процедур через стек Ext.Direct.RPC
'''
@csrf_exempt
def rpc_call_handler(request):
    return RPC().router().rpc_call(request)
    

'''
View для получения списка процедур, доступных для вызова через стек Ext.Direct.RPC
'''
@csrf_exempt
def api_call_handler(request):
    return RPC().api().api_call(request)


'''
Возвращает список URL для работы Ext.Direct.RPC стека
'''
def extdirect_rpc_urls():
    return [
            url(r'^%s$' % escape(settings.EXT_DIRECT_RPC_MOUNTPOINT.lstrip('/')), 'extdirectrpc.views.rpc_call_handler'),
            url(r'^%s/api/$' % escape(settings.EXT_DIRECT_RPC_MOUNTPOINT.lstrip('/').rstrip('/')), 'extdirectrpc.views.api_call_handler'),
            ]
