from abc import abstractmethod


class ERC_20:

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def symbol(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def decimals(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def total_supply(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def balance_of(self, address_owner) -> int:
        raise NotImplementedError

    @abstractmethod
    def transfer(self, address_to, _value) -> bool:
        raise NotImplementedError

    @abstractmethod
    def transfer_from(self, address_from, address_to, _value) -> bool:
        raise NotImplementedError

    @abstractmethod
    def approve(self, address_spender, _value) -> bool:
        raise NotImplementedError

    @abstractmethod
    def allowance(self, address_owner, address_spender) -> int:
        raise NotImplementedError
