
from extdirectrpc.action import ExtDirectRPCAction as RPCAction


class TestAction(RPCAction):

    def doEcho(self, data, request):
        return data

    def multiply(self, num, request):
        try:
            return int(num)*8
        except ValueError:
            raise Exception('Call to multiply with a value that is not a number')
