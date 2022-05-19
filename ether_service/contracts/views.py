import logging
import json

from brownie.exceptions import RPCRequestError
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from mongoengine import OperationError

from contracts.services.service import contractService

_service_ = contractService
logger = logging.getLogger(__name__)


@csrf_exempt
def deploy(request) -> HttpResponse:
    try:
        _response_ = _service_.deploy(request)
    except RPCRequestError as rpc:
        logger.exception(str(rpc.args))
        return HttpResponseBadRequest(reason=rpc.args)
    except OperationError as oe:
        logger.exception(str(oe.args))
        return HttpResponseBadRequest(reason=oe.args)
    except Exception as exc:
        logger.exception(str(exc.args))
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_response_)


@csrf_exempt
def contract_by_address(request) -> HttpResponse:
    try:
        _response_ = _service_.contract_by_address(request)
    except BaseException as exc:
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_response_)


@csrf_exempt
def contracts_by_owner(request) -> HttpResponse:
    try:
        _response_ = _service_.contracts_by_owner(request)
    except BaseException as exc:
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_response_)


@csrf_exempt
def load_contract_and_set_to_cache(request) -> HttpResponse:
    try:
        response = _service_.load_contract(request)
    except ValueError as err:
        return HttpResponseBadRequest(reason=err.args)
    return HttpResponse(response)


@csrf_exempt
def start_ether_service(request) -> HttpResponse:
    logger.info("START_ETHER_SERVICE_REQUEST")
    return HttpResponse("START_ETHER_SERVICE_RESPONSE")
