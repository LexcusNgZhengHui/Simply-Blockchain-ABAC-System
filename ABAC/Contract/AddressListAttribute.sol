// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AddressLister {
    // Array to store the list of addresses
    address[] public addressList;


    // ========== EVENTS ==========
    event AddressRecorded(address indexed userAddress_Rec);



    // Function to add an address to the list
    function addAddress() public {
        // Check if the address is not already added
        for (uint i = 0; i < addressList.length; i++) {
            require(addressList[i] != msg.sender, "Address already added.");
        }
        // Add the address to the list
        addressList.push(msg.sender);
        emit AddressRecorded(msg.sender);
    }

    // Function to get the list of addresses (public getter)
    function getAddresses() public view returns (address[] memory) {
        return addressList;
    }

    // Optional function to get the number of addresses
    function getAddressCount() public view returns (uint) {
        return addressList.length;
    }




}
