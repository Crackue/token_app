import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ether_accounts.services import accounts_services

logger = logging.getLogger(__name__)
_service_ = accounts_services.service


@csrf_exempt
def add(request) -> HttpResponse:
    res = _service_.add(request)
    return HttpResponse(res)


def at(request) -> HttpResponse:
    # TODO
    return HttpResponse()


def connect_to_clef(request) -> HttpResponse:
    # TODO
    return HttpResponse()


def disconnect_from_clef(request) -> HttpResponse:
    # TODO
    return HttpResponse()


def from_mnemonic(request) -> HttpResponse:
    # TODO
    return HttpResponse()


def load(request) -> HttpResponse:
    # TODO
    return HttpResponse()


def remove(request, address: str) -> HttpResponse:
    _service_.remove(address)
    # TODO
    return HttpResponse()


def clear(request) -> HttpResponse:
    res = _service_.clear()
    print(request.session['key'])
    return HttpResponse(res)


@csrf_exempt
def is_local_account(request) -> HttpResponse:
    response = _service_.is_local_account(request)
    return HttpResponse(response)
