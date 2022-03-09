import logging
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from contracts.services.service import contractService

_service_ = contractService
logger = logging.getLogger(__name__)


@csrf_exempt
def deploy(request) -> HttpResponse:
    try:
        _response_ = _service_.deploy(request)
    except BaseException as exc:
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
def load_contract_and_set_to_cache(request) -> HttpResponse:
    response = _service_.load_contract(request)
    return HttpResponse(response)
