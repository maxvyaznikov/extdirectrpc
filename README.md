extdirectrpc
============

django-extdirectrpc is a package to make RPC bridge between ExtJS (throw Ext.Direct) and Django. 

1. Install extdirectrpc
2. Add next lines into urls.py:

from extdirectrpc.views import extdirect_rpc_urls
urlpatterns += extdirect_rpc_urls()

3. Add next line into settings.py:

EXT_DIRECT_RPC_MOUNTPOINT = '/router/'

4. Add next line into TEMPLATE_CONTEXT_PROCESSORS:

'extdirectrpc.context_processors.global_vars',

5. Add next line into template:

<script src="{{ EXT_DIRECT_ROUTER_API_URL }}"></script>

6. Create rpc.py in submodule with new lines for testing:

from extdirectrpc.action import ExtDirectRPCAction as RPCAction


class TestAction(RPCAction):

    def doEcho(self, data, request):
        return data

7. Append to template your js filewith next line:

Ext.direct.Manager.addProvider(EXT_DIRECT_RPC_PROVIDER);

8. Now function doEcho available by path Remote.TestAction.doEcho
