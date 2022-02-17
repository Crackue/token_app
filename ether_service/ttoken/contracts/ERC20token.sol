pragma solidity ^0.8.11;

// SPDX-License-Identifier: MIT

import "../../OpenZeppelin/openzeppelin-contracts@4.3.3/contracts/token/ERC20/ERC20.sol";
import "../../OpenZeppelin/openzeppelin-contracts@4.3.3/contracts/utils/math/SafeMath.sol";

contract ERC20token is ERC20 {
    constructor(uint256 initialSupply, string memory name_, string memory symbol_) ERC20(name_, symbol_) {
        _mint(msg.sender, initialSupply);
    }
}