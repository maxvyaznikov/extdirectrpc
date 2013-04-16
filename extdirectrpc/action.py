# coding=utf-8

'''
Copyright 2012-2013-2013

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
Класс-предок для публикуемых RPC actions
@authors: obraztsov, Max Vyaznikov
'''

import numbers
from django.utils import simplejson
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist



class ExtDirectRPCAction(object):
    
    '''
    Классы, публикующие RPC вызовы должны наследовать класс ExtDirectRPCAction.
    
    Все публичные (не приватные) методы этого класса будут доступны
    для клиента при помощи Ext.Direct
    '''
    
    ## Basic ExtJS params
    
    '''
    Function for organize common ExtJS sorting
    @param query is a QuerySet to use ordering
    @param data is request's input data
    @param default is a default value for sorting, if data will haven't contain
            expected param
    @param aliases (dict) is may used to replace some fields for another,
            'date_short' to 'date', for example, or 'human_name' to 'first_name'
    '''
    @staticmethod
    def __grid_sort__(query, data, default='id', aliases={}):
        sort_name = data.get('sort', default)
        sort_name = aliases.get(sort_name, sort_name)
        if data.get('dir', 'DESC') == 'DESC':
            sort_name = '-'+ sort_name
        return query.order_by(sort_name)
    
    @staticmethod
    def __grid_paging__(query, data):
        start = data.get('start', 0)
        limit = data.get('limit', settings.EXT_DIRECT_RPC_PAGE_SIZE)
        return query.all()[start:start+limit]
    
    
    ## Filters
    
    @staticmethod
    def __filter__(query, field, value):
        if value is not None and value != '':
            return query.filter(**{ field: value })
        else: # if value is None then nothing
            return query
    
    @staticmethod
    def __auto_filter__(query, field, data, default_value=None):
        if field.endswith('__in'):
            value = data.get(field, None)
            if value:
                if not isinstance(value, list):
                    if not isinstance(value, numbers.Integral):
                        int_list = []
                        for i in value.split(','):
                            if i:
                                int_list.append(int(i))
                    else:
                        int_list = [value]
                    value = int_list
            else:
                value = default_value
        else:
            value = data.get(field, default_value)
        return ExtDirectRPCAction.__filter__(query, field, value)
    
    
    ## Edit fields
    
    @staticmethod
    def __auto_edit_field__(obj, field_name, data):
        value = data.get(field_name)
        if value is not None:
            setattr(obj, field_name, value)
    
    '''
        Then in @param obj used ManyToManyField with @param model
        and you need to form youown queryset to insert
        example:
            
            perms = data.get('permissions')
            entries = set()
            for p in perms:
                app_label, codename = p.split('.')
                permissions = Permission.objects.filter(
                                        content_type__app_label=app_label, \
                                        codename=codename)
                for permission in permissions.all():
                    entries.add(permission)
            ExtDirectRPCAction.__manual_edit_m2m_field__(user, 'user_permissions', \
                                        entries, data.get('permissions'))
        
        where user is a standart django User object
    '''
    @staticmethod
    def __manual_edit_m2m_field__(obj, obj_field_name, entries, is_clear=True):
        related = getattr(obj, obj_field_name)
        if is_clear:
            related.clear()
        for e in entries:
            related.add(e)
    
    '''
        Then in @param obj used ManyToManyField with @param model
        example:
            
            ExtDirectRPCAction.__edit_m2m_field__(e, 'statuses', EnterpriseStatus, estatuses)
        
        where e is instance of model with:
            
            statuses = models.ManyToManyField(EnterpriseStatus, \
                        blank=True, null=True, default=None)
    '''
    @staticmethod
    def __edit_m2m_field__(obj, obj_field_name, model, ids, is_clear=True, id_property='id'):
        if ids:
            if isinstance(ids, basestring): ## i.e '34,45,56,67'
                ids = ids.split(',')
            elif isinstance(ids, (int, long)): ## i.e. just 34
                ids = [ids]
            elif isinstance(ids, dict): ## i.e. {id: 34, name: 'Foo',..}
                ids = ids.get(id_property)
                if ids:
                    ids = [ids]
            elif isinstance(ids, list) and isinstance(ids[0], dict): ## i.e. [{id: 34, name: 'Foo',..}, {...}, ...]
                ids = [item.get(id_property) for item in ids]
            ## here ids must be a list of ints, i.e. [34, 45, 56, 67]
            ## or strings, i.e. ['34', '45', '56', '67'], no matter
            entries = model.objects.filter(**{ 'id__in': ids })
            if entries:
                ExtDirectRPCAction.__manual_edit_m2m_field__(obj, obj_field_name, entries, is_clear)
    
    '''
        Then in @param obj used ForeignKey to @param model
        example: 
            
            ExtDirectRPCAction.__edit_m2o_field__(e, 'region', Region, data)
        
        where e is instance of model with 
            
            region = models.ForeignKey(Region, null=True, default=None)
    '''
    @staticmethod
    def __edit_m2o_field__(obj, obj_field_name, model, data, id_property='id'):
        id = data.get(obj_field_name)
        if id:
            if isinstance(id, dict): ## i.e. {id: 34, name: 'Foo',..}
                id = id.get(id_property)
            try:
                value = model.objects.get(id=id)
                setattr(obj, obj_field_name, value)
            except ObjectDoesNotExist:
                pass
    
    @staticmethod
    def __edit_m2m_field_from_json__(obj, obj_field_name, obj_related, data):
        try:
            data = simplejson.loads(data)
        except (ValueError, KeyError, IndexError):
            raise Exception('Incorrect JSON')
        related = getattr(obj, obj_field_name)
        if data['new']:
            for el in data['new']:
                if 'id' in el:
                    del el['id']
                related.create(**el)
        if data['updated']:
            for el in data['updated']:
                try:
                    element = obj_related.objects.get(id=el['id'])
                except:
                    continue
                for key, value in el.iteritems():
                    if key != 'id':
                        setattr(element, key, value)
                element.save()
        if data['removed']:
            for id in data['removed']:
                try:
                    element = obj_related.objects.get(id=id)
                except:
                    continue
                element.delete()

    ###


