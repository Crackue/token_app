import json
import logging
from abc import ABC, abstractmethod
from contracts.services.repository import repository
from utils import base_utils

logger = logging.getLogger(__name__)


class ContractServices(ABC):
    @abstractmethod
    def deploy(self, request):
        raise NotImplementedError


class ContractServicesImpl(ContractServices):
    def deploy(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        contract_name = post["contract_name"]
        contract_symbol = post["contract_symbol"]
        contract_supply = post["contract_supply"]
        contract_supply_val = base_utils.get_num_with_decimals(contract_supply, 18)
        repository.deploy(address_owner, contract_name, contract_symbol, contract_supply_val)


contractService = ContractServicesImpl()
