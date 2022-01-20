from django.http import HttpResponse

from ether_network import bch_connection

connectionImpl = bch_connection.BCHConnectionImpl()


def connect(request):
    return HttpResponse(connectionImpl.connect())


def disconnect(request):
    return HttpResponse(connectionImpl.disconnect())


def gas_limit(request):
    pass


def gas_price(request):
    pass


def is_connected(request):
    return HttpResponse(connectionImpl.isConnected())


def show_active(request):
    return HttpResponse(connectionImpl.showActive())
