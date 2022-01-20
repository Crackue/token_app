pragma solidity ^0.8.7;

// SPDX-License-Identifier: MIT

import "../../OpenZeppelin/openzeppelin-contracts@4.3.3/contracts/token/ERC20/ERC20.sol";
import "../../OpenZeppelin/openzeppelin-contracts@4.3.3/contracts/utils/math/SafeMath.sol";

contract ERC20token is ERC20 {
    constructor(uint256 initialSupply) ERC20("TToken", "TTK") {
        _mint(msg.sender, initialSupply);
    }
}