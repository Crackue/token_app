pragma solidity ^0.8.11;

import "../../OpenZeppelin/openzeppelin-contracts@4.3.3/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "../../OpenZeppelin/openzeppelin-contracts@4.3.3/contracts/utils/Counters.sol";


// SPDX-License-Identifier: MIT

contract ERC721token is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721("NFToken", "TIK") {}

    function awardItem(address to, string memory tokenURI)
        public
        returns (uint256)
    {
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(to, newItemId);
        _setTokenURI(newItemId, tokenURI);

        return newItemId;
    }
}
