// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./AdminControl.sol";
contract SubjectAttributes is AdminControl {

    // ========== DATA STRUCTURES ==========
    struct UserAttribute {
            string role;
            uint256 clearanceLevel;
            bool isActive;
        }

    struct ResourcesAttributes{
        string assetType;
        uint256 sensitiveLevel;

    }

    // ========== STATE VARIABLES ==========
    //Variables whose values are permanently stored in a contract storage.

    // address public admin; //stores the Ethereum address of an administrator
    mapping(address => UserAttribute) public users; //associate address to userattribute
    mapping(string => ResourcesAttributes) public resources; //associate string value to resorucesattributes


    // ========== EVENTS ==========
    //Emit logs to track changes in the contract
    //An event is a special kind of log that a contract can emit. Events are used to notify external listeners (like dApps or other contracts) that something has happened in the smart contract
    //function , function name ,parameter
    event UserCreation(address userCreate); //When the UserUpdated event is emitted, the address of the user whose data was updated will be logged, and external applications can listen to this event to react accordingly (for example, update the UI to reflect the changes).
    event ResourcesCreation (string resourceCreate);


     // ========== MODIFIERS ==========
    //Restricts functions to the admin address
    //function, function name, parameter
    //virtual keyword is used in the base contract to make the function or modifier open for overriding in child contracts.
    // modifier onlyAdmin() virtual {
    //     //condition ,if .........; else:......
    //     require(msg.sender == admin, "Only admin can call this");
    //     //don't forget this to let system know
    //     _;
    // }

    // ========== CONSTRUCTOR ==========
    //Only perform 1time when deploy smartcontract
    // constructor() {
    //     admin = msg.sender;
    // }

    ///Function///
    // ========== USER MANAGEMENT ==========
    //        functionname, parameter to get
    function CreateUser (address userAddress, string memory role, uint256 clearnancelevel) external onlyAdmin {
    //mapping users and address= userattribute info
    //the reason why "true" is becasue the bool isactive, default set to true
        users[userAddress] = UserAttribute(role,clearnancelevel, true);
        //create log using the Event function emit the data
        emit UserCreation(userAddress);

    }
    
    function DeactiveUser (address userAddress ) public onlyAdmin{
        users[userAddress].isActive = false;
        emit UserCreation(userAddress);
    }

    function ChangeUserRoles (address userAddress,string memory role) public onlyAdmin{
        users[userAddress].role = role;
        emit UserCreation(userAddress);


    }

    // ========== Resources MANAGEMENT ==========
    function CreateResources (string memory resourcesID, string memory assetType , uint256 sensitiveLevel) public onlyAdmin{
        resources[resourcesID] = ResourcesAttributes(assetType,sensitiveLevel); 
        emit ResourcesCreation (resourcesID);
    }

    function ModifyResources (string memory resourcesID, string memory assetType , uint256 sensitiveLevel) public onlyAdmin{
        resources[resourcesID] = ResourcesAttributes(assetType,sensitiveLevel); 
        emit ResourcesCreation (resourcesID);
    }
    



    



}

