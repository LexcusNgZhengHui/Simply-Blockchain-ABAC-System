// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./AdminControl.sol";

contract PolicyManagement is AdminControl{

    //Data structure //
    struct Policy {
        string PolicyID;
        string Description;
        Condition[] conditions; //An array of 'Condition' objects associated with the policy
        bool isActive;
        
    }

      struct Condition {
        //sample format when key-in
        //[[ "user", "role" , "==" , "admin"] ]
        string attributeType; // "user", "resource", or "environment"
        string attributeName; // e.g., "role", "sensitivityLevel"
        string operator; // "==", ">=", etc.
        string value;
    }

     // ========== STATE VARIABLES ==========
    // address public admin;
    mapping(address => bool) public policyAdmins;
    mapping(string => Policy) public policies;
    string[] public policyIds;


    // ========== EVENTS ==========
    event PolicyAdminModify (address policyadminModify );
    event PolicyCreated(string policyId);
    event PolicyToggled(string policyId, bool isActive);


    // ========== MODIFIERS ==========
    // modifier onlyAdmin()virtual  {
    //     require(msg.sender == PMadmin, "Only admin can call this");
    //     _;
    // }

    modifier onlyPolicyAdmin() {
        require(policyAdmins[msg.sender], "Only policy admin can call this");
        _;
    }

      // ========== CONSTRUCTOR ==========
    // constructor() {
    //     admin = msg.sender;
    // }
    //============ Policy Admin Manageent ==============
    function GrantPolicyAdmin(address UserAddress) public onlyAdmin{
        policyAdmins[UserAddress] = true;
        emit PolicyAdminModify(UserAddress);
    }

    function RevokePolicyAdmin(address UserAddress) public onlyAdmin{
        policyAdmins[UserAddress] = false;
        emit PolicyAdminModify(UserAddress);
    }

    //=========== Policy Management ==============

    function CreatePolicy (string memory _policyID, string memory _policydescription,  Condition[] memory _conditions)public onlyPolicyAdmin{
        Policy storage policyd = policies[_policyID];
        policyd.PolicyID =_policyID;
        policyd.Description=_policydescription;
        policyd.isActive = true;
        

         for (uint256 i = 0; i < _conditions.length; i++) {
            policyd.conditions.push(_conditions[i]);
            
        }

        policyIds.push(_policyID);
        emit PolicyCreated(_policyID);

    }

    function TongglePolicy (string memory policy_ID, bool _isactive)public  onlyPolicyAdmin {
        policies[policy_ID].isActive =_isactive;
        emit PolicyToggled(policy_ID, _isactive);


    }

    function GetAllPolicies()public view returns(string[] memory){
        return policyIds;
    }





}