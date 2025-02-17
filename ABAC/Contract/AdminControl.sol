// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdminControl {
    address public admin;

    modifier onlyAdmin() virtual {
        require(msg.sender == admin, "Only admin can call this");
        _;
    }

    constructor() {
        admin = msg.sender;
    }
}