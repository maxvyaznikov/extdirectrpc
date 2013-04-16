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
Основной управляющий модуль Ext.Direct.RPC стека
@authors: obraztsov, Max Vyaznikov
'''

from django.conf import settings
from dispatcher import ExtDirectDispatcher
from router import Router
from api import API
from action import ExtDirectRPCAction
from inspect import getmembers, ismethod, isclass
from django.utils.log import logger
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


class RPC(object):
    
    def __init__(self):
        self.dispatcher_instance = ExtDirectDispatcher()
        self.set_base_url(settings.EXT_DIRECT_RPC_MOUNTPOINT) 
        self.discover_rpc_calls()
        self.router_instance = Router(self.dispatcher())
        self.api_instance = API(self.dispatcher(), self.get_base_url())
        
        
    def router(self):
        '''
        Возвращает экземпляр класса Router
        '''
        
        return self.router_instance
        
        
    def api(self):
        '''
        Возвращает экземпляр класса API
        '''
        
        return self.api_instance
    
    
    def dispatcher(self):
        '''
        Возвращает экземпляр класса ExtDirectDispatcher
        '''
        
        return self.dispatcher_instance
        
        
    def set_base_url(self, url):
        '''
        Устанавливает url по которому доступен router
        '''
        
        self.base_url = url
        
        
    def get_base_url(self):
        '''
        Возвращает url по которому доступен router
        '''
        
        return self.base_url
        
           
    def discover_rpc_calls(self):
        '''
        Поиск RPC actoins в установленных модулях
        '''
        
        # Для всех установленных приложений
        for application_path in settings.INSTALLED_APPS:
            # Пытаемся выполнить импорт
            application = import_module(application_path)
            
            '''
            Если в приложении есть модуль с именем rpc.py,
            значит возможно приложение предоставляет некоторые из
            своих классов для удаленного вызова
            '''
            try:
                rpc_module = import_module('%s.rpc' % application_path)
                
                '''
                Для всех классов из модуля, если они расширяют класс
                ExtDirectRPCAction, регистрируем в списке API их
                публичные (не приватные) вызовы
                '''
                try:
                    for class_name, class_class in getmembers(rpc_module, isclass):
                    
                        try:
                            if issubclass(class_class, ExtDirectRPCAction):
                            
                                # Создаем экземпляр класса Action
                                class_instance = class_class()
                                
                                # Регистрируем все его методы, не являющиеся приватными
                                for method_name, method in getmembers(class_instance, ismethod):
                                
                                    # Имена приватных методов начинаются с символа '_'
                                    if not method_name.startswith('_'):
                                        # Если метод не приватный, регистрируем его
                                        self.dispatcher().register_method(class_name, method_name, method)
                                        
                        except Exception, e:
                            logger.error(e)
                            
                except Exception, e:
                    logger.error(e)        
                    
            except:
                '''
                Сюда мы попадаем, если не смогли импортировать модуль rpc.py
                Возможно, этого модуля просто не существует в установленном приложении,
                но если он существует и при этом не импортирован, значит что-то пошло не так.
                '''
                if module_has_submodule(application, 'rpc'):
                    raise
        
