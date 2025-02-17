import json
from web3 import Web3
from solcx import compile_files
import os

# Set up Ganache connection
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
if not w3.is_connected():
    print("[ERROR] Connection Failed!!!!")
    exit()
print("[SUCCESS] Connected to Ganache!!!\n")

# Set default account
w3.eth.default_account = w3.eth.accounts[0]
print(w3.eth.default_account)

# Compile contracts
contract_files = [
    '../Contract/ABAC.sol',
    '../Contract/AddressListAttribute.sol',
    '../Contract/AdminControl.sol',
    '../Contract/PolicyManagement.sol',
    '../Contract/SubjectAttribute.sol'
]

print("Compiling Solidity files...")
compiled_sol = compile_files(contract_files)
print("Compilation completed successfully!\n")

# Create folder for ABIs if it doesn’t exist
ABI_DIR = "compiled_ABIs"
os.makedirs(ABI_DIR, exist_ok=True)


# Deployment function
def deploy_contract(contract_identifier):
    try:
        # Extract contract data
        contract_data = compiled_sol[contract_identifier]
        contract_name = contract_identifier.split(':')[-1]
        
        print(f"[DEPLOYING] Deploying {contract_name}...")
        
        # Get ABI and bytecode
        abi = contract_data['abi']
        bytecode = contract_data['bin']

         # Save ABI to a JSON file
        abi_path = f"{ABI_DIR}/{contract_name}.json"
        with open(abi_path, 'w') as abi_file:
            json.dump(abi, abi_file, indent=4)
        print(f"[INFO] ABI saved to {abi_path}")

    
        # Deploy contract
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"[SUCCESS] {contract_name} Successfully Deployed!!!")
        print(f"[INFO] Contract Address: {tx_receipt.contractAddress}\n")
        return tx_receipt.contractAddress
    
    except Exception as e:
        print(f"[ERROR] Failed to deploy {contract_name}: {str(e)}")
        return None

# Deploy contracts in required order (handle dependencies first)
deployed_addresses = {}
contract_identifiers = [
    # List contracts in deployment order
    '../Contract/SubjectAttribute.sol:SubjectAttributes',
    '../Contract/AddressListAttribute.sol:AddressLister',
    '../Contract/AdminControl.sol:AdminControl',
    '../Contract/PolicyManagement.sol:PolicyManagement',
    '../Contract/ABAC.sol:ABAC'
]

for identifier in contract_identifiers:
    if identifier in compiled_sol:
        address = deploy_contract(identifier)
        if address:
            contract_name = identifier.split(':')[-1]
            deployed_addresses[contract_name] = address

# Save addresses to file
with open('deployed_addresses.json', 'w') as f:
    json.dump(deployed_addresses, f, indent=4)

print("Deployment Summary:")
for contract, address in deployed_addresses.items():
    print(f"{contract}: {address}")