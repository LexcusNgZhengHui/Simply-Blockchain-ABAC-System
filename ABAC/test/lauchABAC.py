import json
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import os

#will use this for load the .env file
from dotenv import load_dotenv
load_dotenv()



  


#Connect to Ganachess

w3= Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chaind_id = 1337
assert w3.is_connected(), "Failed to connect to Ganache!"

# Set default account (use the first Ganache account)
private_key ="0xa1290a55c286f1f174e1891df818922cc6a928b562b267e96f65f3e325332233"
my_address="0x29006e70481b47d9264B2E45E85e58C52b5eE079"
w3.eth.default_account=my_address

# Compile the ABAC contract
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

sources = {
    "ABAC.sol": {"content": read_file("ABAC.sol")},
    "SubjectAttribute.sol": {"content": read_file("SubjectAttribute.sol")},
    "PolicyManagement.sol": {"content": read_file("PolicyManagement.sol")},
    "AdminControl.sol": {"content": read_file("AdminControl.sol")},
    "AddressListAttribute.sol": {"content": read_file("AddressListAttribute.sol")}
}

# Compile all contracts together
install_solc("0.8.0")
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": sources,
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "evm.bytecode"]}
        }
    }
})
#print(compiled_sol)

with open("compiled_code.json","w") as file:
    json.dump (compiled_sol,file)

# Get contract ABI and bytecode
abi = compiled_sol["contracts"]["ABAC.sol"]["ABAC"]["abi"]
bytecode = compiled_sol["contracts"]["ABAC.sol"]["ABAC"]["evm"]["bytecode"]["object"]


# Deploy the contract
abac_main =w3.eth.contract(abi=abi,bytecode=bytecode)
print(abac_main)
nonce=w3.eth.get_transaction_count(my_address)
print (nonce)
tx_hash = abac_main.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt["contractAddress"]
abac = w3.eth.contract(address=contract_address, abi=abi)


