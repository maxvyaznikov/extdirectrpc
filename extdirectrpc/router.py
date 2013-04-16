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
Класс обработки запросов Ext.Direct стека.
@authors: obraztsov, Max Vyaznikov
'''
import sys
import traceback

from django.http import HttpResponse
from django.utils import simplejson
# from django.core import serializers
from json import ExtDirectDjangoJSONEncoder


class Router(object):

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher


    def rpc_call(self, request):
        '''
        Обработчик RPC вызовов
        '''
        
        post = request.POST
    
        '''
        Обработка форм и загрузка файлов.
        
        Не протестированы должным образом.
        При использовании обратить особое внимание.
        '''    
        if post.get('extAction'):
            # Вызов от обработчика формы Ext.form.Form сопровождается следующими полями:
            requests = {
                'action': post.get('extAction'),
                'method': post.get('extMethod'),
                'data': [post],
                'upload': post.get('extUpload') == 'true',
                'tid': post.get('extTID')
            }   
            
            # Наличие поля extUpload говорит о том, что в запросе были переданы файлы
            if requests['upload']:
                # Обработка загрузки файла
                output = simplejson.dumps(self._handle_call(requests, request))
                return HttpResponse('<textarea>%s</textarea>' % output)
          
        else:
            '''
            Обработка списка RPC-транзакций не связанных с обработкой форм
            ''' 
            try:
                requests = simplejson.loads(request.POST.keys()[0])
            except (ValueError, KeyError, IndexError):
                requests = []      
                    
        '''
        Если передана только одна транзакция, преобразуем ее в массив транзакций
        '''          
        if not isinstance(requests, list):
            requests = [requests]
        
        '''
        Вызываем обработчик вызовов для каждой транзакции
        '''
        output = [self._handle_call(request_data, request) for request_data in requests]
        
        '''
        Сериализуем ответ
        '''
        serialized_response = simplejson.dumps(output, cls=ExtDirectDjangoJSONEncoder)
        # serialized_response = serializers.serialize('json', output)
            
        # Возвращаем ответ
        return HttpResponse(serialized_response, mimetype="application/json")
    
    
    def _handle_call(self, request_data, request):
        '''
        Обработчик вызова процедуры
        '''
        
        '''
        Получаем имя метода
        '''
        method = request_data['method']
        action = request_data['action']
        method_full_path = action + '.' + method
        
        '''
        Проверяем доступность метода
        '''
        if not (method_full_path in self._dispatcher.registered_methods()):
            # Если метод недоступен, возвращаем для этой транзакции исключение
            return {
                'tid': request_data['tid'],
                'type': 'exception',
                'action': request_data['action'],
                'method': method,
                'message': 'Undefined action class'
            }
        
        
        '''
        Формируем список параметров для метода
        '''
        arguments = request_data.get('data') or []
        
        # Добавляем request в список передаваемых методу дополнительных именованных параметров
        extra_arguments = {
                            'request': request
                            }
        
        '''
        Получаем указатель на функцию
        '''
        function = self._dispatcher.registered_methods()[method_full_path]   
        
        '''
        Вызываем функцию.
        
        Мы не проверяем правильность передачи параметров и их типы.
        Если мы передадим функции список параметров, который она не сможет обработать,
        мы получим исключение и возвратим информацию о нем вместо ответа функции
        '''
        try:
            # Пробуем вызвать метод
            return {
                'tid': request_data['tid'],
                'type': 'rpc',
                'action': request_data['action'],
                'method': method,
                'result': function(*arguments, **extra_arguments)
            }
        except Exception, e:
            # Если по какой либо причине вызов метода не состоялся, возвращаем информацию об исключении
            type_, value_, traceback_ = sys.exc_info()
            return {
                'tid': request_data['tid'],
                'type': 'exception',
                'action': request_data['action'],
                'method': method,
                'message': str(e),
                'traceback': traceback.format_exception(type_, value_, traceback_)
            }
