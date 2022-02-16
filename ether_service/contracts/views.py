import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from contracts.services.service import contractService

_service_ = contractService
logger = logging.getLogger(__name__)


@csrf_exempt
def deploy(request) -> HttpResponse:
    _response_ = _service_.deploy(request)
    return HttpResponse(_response_)
