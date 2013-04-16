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
Класс конфигурации Ext.Direct стека.
@authors: obraztsov, Max Vyaznikov
'''

from inspect import ismethod, getargspec


class ExtDirectDispatcher(object):
   
    def __init__(self):
        self.actions = {}
        self.method_list = {}
        self.base_url = ''

        
    def get_method_len(self, method):
        '''
        Получение количества параметров метода
        '''
        
        # Получаем списки параметров, требуемых для функции
        arguments, parguments, pkwarguments, defaults = getargspec(method)
        
        length = 0
        request_found = False
        
        # Увеличиваем счетчик требуемых параметров
        if arguments <> None:
            length += len(arguments)
        
        '''
        Не учитываем параметр self и параметр request,
        которые будут подставлены автоматически при вызове
        '''
        for name in arguments:
            if name == 'self':
                length -= 1
            if name == 'request':
                length -= 1
                request_found = True
        
        # Увеличиваем счетчик требуемых параметров     
        if parguments <> None:
            length += len(parguments)
        
        # Увеличиваем счетчик требуемых параметров     
        if pkwarguments <> None:
            length += len(pkwarguments)
        
        '''
        Функция должна принимать request в качестве своего параметра.
        Если это не так, выкидываем исключение TypeError
        '''
        if not request_found:
            raise TypeError()
            
        return length

        
    def register_method(self, action_name, method_name, method):
        '''
        Добавление метода в список доступных для вызова
        '''
        
        if not ismethod(method):
            raise TypeError()
        
        # Получаем полный путь вида "Action.Method"
        full_method_path = action_name + '.' + method_name
        self.method_list[full_method_path] = method
        
        # Если мы ранее не регистрировали методы из данного Action
        if not self.actions.has_key(action_name):
            # Инициализируем для этого Action новый массив
            self.actions[action_name] = []
         
        # Регистрируем метод    
        self.actions[action_name].append({
                                          "name": method_name,
                                          "len": self.get_method_len(method)
                                          })


    def actions_list(self):
        '''
        Получение списка зарегистрированных классов Action
        '''
        
        return self.actions

        
    def registered_methods(self):
        '''
        Получение списка зарегистрированных методов
        '''
        
        return self.method_list

