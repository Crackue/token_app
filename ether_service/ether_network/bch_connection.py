import logging

import brownie
from abc import abstractmethod
from pathlib import Path

from ether_service.settings import BASE_DIR, CONTRACT_HOME
from brownie import project

logger = logging.getLogger(__name__)


class BCHConnection:

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def gas_limit(self):
        raise NotImplementedError

    @abstractmethod
    def gas_price(self):
        raise NotImplementedError

    @abstractmethod
    def is_connected(self):
        raise NotImplementedError

    @abstractmethod
    def show_active(self):
        raise NotImplementedError


class BCHConnectionImpl(BCHConnection):

    def __init__(self):
        self.connector = BCHConnector()

    def connect(self):
        try:
            if not brownie.network.is_connected():
                brownie_config_path = Path(str(CONTRACT_HOME))
                brownie._config._load_project_config(brownie_config_path)
                logger.info("BCHConnectionImpl.connect() CONFIG: " + str(brownie.network.state.CONFIG.settings))
                brownie.network.connect()
                if brownie.network.is_connected():
                    logger.info("Connection to " + self.connector.server + " established successfully")
                    if not project.get_loaded_projects():
                        project.load(brownie_config_path, "TtokenProject")
                    logger.info("Contract compilation finished successfully")
                    return True
                else:
                    logger.info("Connection to " + self.connector.server + " FAILED!!!")
                    return False
        except Exception as exc:
            logger.exception(exc)

    def disconnect(self):
        # TODO try catch and logs
        if brownie.network.is_connected():
            brownie.network.disconnect()
            return True
        else:
            False

    def gas_limit(self):
        # TODO
        pass

    def gas_price(self):
        # TODO
        pass

    def is_connected(self):
        return brownie.network.is_connected()

    def show_active(self):
        return brownie.network.show_active()


class BCHConnector(object):

    def __init__(self):
        # TODO
        self.server = 'default'


bch_connection = BCHConnectionImpl()
