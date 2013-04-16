# coding=utf-8

from django.conf import settings

def global_vars(request):
    return {
            'EXT_DIRECT_ROUTER_API_URL': settings.EXT_DIRECT_RPC_MOUNTPOINT + 'api/',
            }
