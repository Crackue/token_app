import logging
from brownie.exceptions import UnknownAccount
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from mongoengine import OperationError

from erc20.services.service import serviceRest

_service_ = serviceRest
logger = logging.getLogger(__name__)


def name(request) -> HttpResponse:
    try:
        _name_ = _service_.name(request)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_name_)


def symbol(request) -> HttpResponse:
    try:
        _symbol_ = _service_.symbol(request)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_symbol_)


def decimals(request) -> HttpResponse:
    try:
        _decimals_ = _service_.decimals(request)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_decimals_)


def total_supply(request) -> HttpResponse:
    try:
        _total_supply_ = _service_.total_supply(request)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_total_supply_)


@csrf_exempt
def balance_of(request) -> HttpResponse:
    try:
        balance = _service_.balance_of(request)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(balance)


@csrf_exempt
def transfer(request) -> HttpResponse:
    try:
        _transfer_ = _service_.transfer(request)
    except UnknownAccount as ua:
        logger.exception(str(ua.args))
        return HttpResponseNotFound(reason=ua.args)
    except OperationError as oe:
        logger.exception(str(oe.args))
        return HttpResponseBadRequest(reason=oe.args)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_transfer_)


@csrf_exempt
def transfer_from(request) -> HttpResponse:
    try:
        _transfer_from_ = _service_.transfer_from(request)
    except UnknownAccount as ua:
        logger.exception(str(ua.args))
        return HttpResponseNotFound(reason=ua.args)
    except OperationError as oe:
        logger.exception(str(oe.args))
        return HttpResponseBadRequest(reason=oe.args)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_transfer_from_)


@csrf_exempt
def approve(request) -> HttpResponse:
    try:
        _approve_ = _service_.approve(request)
    except UnknownAccount as ua:
        logger.exception(str(ua.args))
        return HttpResponseNotFound(reason=ua.args)
    except OperationError as oe:
        logger.exception(str(oe.args))
        return HttpResponseBadRequest(reason=oe.args)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_approve_)


@csrf_exempt
def allowance(request) -> HttpResponse:
    try:
        _allowance_ = _service_.allowance(request)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_allowance_)
