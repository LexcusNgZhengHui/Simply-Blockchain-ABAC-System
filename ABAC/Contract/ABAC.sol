// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./PolicyManagement.sol";
import "./SubjectAttribute.sol";
import "./AddressListAttribute.sol";

 //inherit functionality from another contract or interface

contract ABAC is PolicyManagement,SubjectAttributes,AddressLister  {

    //Variable
    //will removethis becauese we inheritance from other contract
    //address admin;

    // ========== MODIFIERS ==========
    //the override here is put for later inheritance by other file
    //the override keyword is used in the derived contract to modify or extend the behavior of the virtual modifier or fun
    modifier onlyAdmin() override  {
        require(msg.sender == admin, "Only admin can call this");
        _;
    }

    //function
    //Check Access Logic
    function checkAccess(address _user, string memory _resourceId) public view returns (bool){
        //Fetching User and Resource Data from other contract
        UserAttribute memory userAtt = users[_user];
        ResourcesAttributes memory resAtt = resources[_resourceId];
        //Check if the User is Active
        require(userAtt.isActive=true,"User is no Active");

        string[]memory activePolicyIds = GetAllPolicies();

        //the for loop iterates over each active policy ID.
        //Policy memory policy = policies[activePolicyIds[i]]; retrieves the policy associated with the ID.
        //If the policy is not active (policy.isActive == false), it is skipped using the continue keyword.
        //This loop iterates over each active policy ID (activePolicyIds[i]).
        for(uint256 i = 0; i < activePolicyIds.length; i++){
        //Inside the loop, the policy data is fetched from the policies mapping using the policy ID. 
        //The data fetched is stored as policyP.

            Policy memory policyP = policies[activePolicyIds[i]];
            //if the current policy is inactive (!policyP.isActive), the loop skips to the next policy (using continue).
             if (!policyP.isActive) continue;

            //assuming that the policy is satisfied
             bool policySatisfied = true;
             //This loop iterates over each condition in the policy. The policy contains an array of conditions 
            for (uint256 j = 0; j < policyP.conditions.length; j++) {
                //For each iteration, the current condition is retrieved from the policyP.conditions array and stored in condition.
                Condition memory condition = policyP.conditions[j];
                
                //This line calls the evaluateCondition function to check if the condition is satisfied. If the condition returns false, it means the condition is not satisfied.
                if (!evaluateCondition(userAtt, resAtt, condition)) {
                    //If any condition is not satisfied, we mark the policySatisfied flag as false.
                    policySatisfied = false;
                    // If a condition fails, we exit the loop early (using break), as we don't need to check further conditions in this policy.
                    break;
                }
            }
            // After evaluating all the conditions in a policy, if all conditions are satisfied (policySatisfied == true), the function returns true, granting access to the resource.
            if (policySatisfied) return true;
        }
        //If none of the policies grant access, the function reaches the end of the loop and returns false.
        return false;
            
        



    }


    function evaluateCondition(UserAttribute memory userAtt,ResourcesAttributes memory resAtt, Condition memory _condition)  internal pure returns ( bool){
        //variable to store the value of the attribute that we need to compare, either from the user or the resource.
        string memory attributeValue;
        //This block checks whether the attributeType in the condition refers to user or resource. 
        //It does so by comparing the keccak256 hash of the string to avoid direct string comparison 
        //(as Solidity does not support direct string comparisons).
        if (keccak256(bytes(_condition.attributeType)) == keccak256(bytes("user"))) {
            // If the condition's attribute is "role", we set attributeValue to the user's role.
            if (keccak256(bytes(_condition.attributeName)) == keccak256(bytes("role"))) {
            attributeValue = userAtt.role;
            //If the condition's attribute is "clearanceLevel", we convert the user's clearanceLevel to a string (since uint cannot be directly compared to strings).
        } else if (keccak256(bytes(_condition.attributeName)) == keccak256(bytes("clearanceLevel"))) {
            attributeValue = uintToString(userAtt.clearanceLevel);
        }
        //If attributeType is "resource", the condition checks for the sensitivityLevel of the resource:
    } else if (keccak256(bytes(_condition.attributeType)) == keccak256(bytes("resource"))) {
        //If the condition's attribute is "sensitivityLevel", we convert the resource's sensitivityLevel to a string.
        if (keccak256(bytes(_condition.attributeName)) == keccak256(bytes("sensitivityLevel"))) {
            attributeValue = uintToString(resAtt.sensitiveLevel);
        }
    }

    }


    function uintToString(uint256 _num) internal pure returns (string memory) {
        //The first if condition checks if the number _num is 0.
        //If _num is 0, the function immediately returns the string "0", because 0 is a special case and doesn't need any further processing.
        if (_num == 0) return "0";
        //The number is copied to a temporary variable temp. This ensures that _num remains unchanged while we manipulate temp to calculate the number of digits.
        uint256 temp = _num;
        //This variable will keep track of how many digits the number has.
        uint256 digits;

        // Calculate the number of digits:
        // The while loop is used to count how many digits the number _num has.
        // temp != 0: The loop continues as long as temp is not zero.
        // digits++: For each iteration, the digits counter is incremented.
        // temp /= 10: The number is divided by 10, which effectively removes the last digit. This process continues until temp becomes zero, at which point we know how many digits the number had.

        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        //Create a buffer to hold the string representation:
        //A new dynamic byte array buffer of size digits is created to hold the string representation of the number. 
        //Each byte will store one character (which will correspond to one digit).
        bytes memory buffer = new bytes(digits);

    //Convert each digit to a character and fill the buffer:
    // The second while loop is used to extract each digit from _num and convert it into a character.
    // _num != 0: The loop continues until _num becomes zero.
    // digits -= 1: The digits counter is decremented to ensure that we fill the buffer from right to left, starting from the least significant digit (rightmost).
    // buffer[digits] = bytes1(uint8(48 + _num % 10));
    // _num % 10: The modulus operation (%) extracts the last digit of _num. For example, if _num is 1234, then 1234 % 10 = 4.
    // uint8(48 + _num % 10): The value 48 is the ASCII code for the character '0'. By adding the last digit (e.g., 4), we get the ASCII code for the corresponding digit character ('4').
    // bytes1(...): This converts the result into a bytes1 (a single byte) and assigns it to the buffer.
    // _num /= 10: After extracting the last digit, we divide _num by 10 to remove the last digit and continue with the next digit.

        while (_num != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + _num % 10));
            _num /= 10;
        }
        //Return the result as a string:
        //Finally, the function returns the buffer as a string by calling string(buffer), which converts the byte array buffer into a string type.
        return string(buffer);
    }

    function stringToUint(string memory _s) internal pure returns (uint256) {
        bytes memory b = bytes(_s);
        uint256 result = 0;
        for (uint256 i = 0; i < b.length; i++) {
            uint256 digit = uint256(uint8(b[i])) - 48;
            require(digit >= 0 && digit <= 9, "Invalid number");
            result = result * 10 + digit;
        }
        return result;
    }

    





}