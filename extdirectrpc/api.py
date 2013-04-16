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
Класс генерации списка API для клиента.
@authors: obraztsov, Max Vyaznikov
'''

from django.http import HttpResponse
from django.utils import simplejson


class API(object):

    def __init__(self, dispatcher, base_url):
        self._dispatcher = dispatcher
        self._base_url = base_url
        
        
    def api_call(self, request):
        '''
        Обработчик вызова запроса списка API
        '''
        
        output = {
                  'url': self._base_url,
                  'enableBuffer': 50,
                  'type': 'remoting',
                  'actions': self._dispatcher.actions_list(),
                  'namespace': 'Remote',
                  }
        
        response = HttpResponse('var EXT_DIRECT_RPC_PROVIDER = %s;' % simplejson.dumps(output), mimetype="application/json")
        return response

