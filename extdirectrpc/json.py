from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads
from django.db import models
from django.db.models.query import QuerySet
from django.utils.functional import curry
from django.core.serializers.json import DjangoJSONEncoder



class ExtDirectDjangoJSONEncoder(DjangoJSONEncoder):
    
    def __serializable__(self, obj):
        return hasattr(obj, 'serialize') and callable(getattr(obj, 'serialize'))
    
    def default(self, obj):
        if isinstance(obj, models.Model):
            if self.__serializable__(obj):
                return obj.serialize()
            else:
                return loads(serialize('json', obj))
        if isinstance(obj, QuerySet):
            list = []
            for o in obj:
                list.append(o.serialize())
            return list
        return DjangoJSONEncoder.default(self, obj)


