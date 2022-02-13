
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from erc20.services.service import serviceRest

_service_ = serviceRest
logger = logging.getLogger(__name__)


def name(request) -> HttpResponse:
    logger.info(request)
    _name_ = _service_.name()
    return HttpResponse(_name_)


def symbol(request) -> HttpResponse:
    logger.info(request)
    _symbol_ = _service_.symbol()
    return HttpResponse(_symbol_)


def decimals(request) -> HttpResponse:
    logger.info(request)
    _decimals_ = _service_.decimals()
    return HttpResponse(_decimals_)


def total_supply(request) -> HttpResponse:
    logger.info(request)
    _total_supply_ = _service_.total_supply()
    return HttpResponse(_total_supply_)


@csrf_exempt
def balance_of(request) -> HttpResponse:
    balance = _service_.balance_of(request)
    return HttpResponse(balance)


@csrf_exempt
def transfer(request) -> HttpResponse:
    _transfer_ = _service_.transfer(request)
    return HttpResponse(_transfer_)


@csrf_exempt
def transfer_from(request) -> HttpResponse:
    _transfer_from_ = _service_.transfer_from(request)
    return HttpResponse(_transfer_from_)


@csrf_exempt
def approve(request) -> HttpResponse:
    _approve_ = _service_.approve(request)
    return HttpResponse(_approve_)


@csrf_exempt
def allowance(request) -> HttpResponse:
    _allowance_ = _service_.allowance(request)
    return HttpResponse(_allowance_)
