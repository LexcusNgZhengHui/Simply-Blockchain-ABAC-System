# Import Modules/Functions
from web3 import Web3
import json

# Connect to Ganache
GANACHE_URL = 'HTTP://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.is_connected():
    print('\n[SUCCESS] CONNECTED TO GANACHE NETWORK\n')
else:
    print("\n[FAILED] FAILED CONNECT TO GANACHE NETWORK\n")

# set first account as default user or "Administrator"
w3.eth.default_account = w3.eth.accounts[0]



#  Load Deployed Contract Addresses
with open('deployed_addresses.json', 'r') as f:
    deployed_addresses = json.load(f)

if "ABAC" not in deployed_addresses:
    print("[ERROR] ABAC contract not found in deployed addresses!")
    exit()

ABAC_ADDRESS = deployed_addresses["ABAC"]
print(f"[INFO] ABAC Contract Address: {ABAC_ADDRESS}")

# Load ABAC Contract ABI file
ABI_FILE = "compiled_ABIs/ABAC.json"
try:
    with open(ABI_FILE, 'r') as f:
        ABAC_ABI = json.load(f)
    print(f"[INFO] ABI loaded from {ABI_FILE}")
except FileNotFoundError:
    print(f"[ERROR] ABI file {ABI_FILE} not found! Ensure you re-run deployment.")
    exit()

# Load ABAC Contract
abac_contract = w3.eth.contract(address=ABAC_ADDRESS, abi=ABAC_ABI)



# Function to Register a User
def register_user(user_address, role, clearance_level):
    try:
        print(f"[INFO] Registering user {user_address} with role '{role}' and clearance level {clearance_level}...")
        tx_hash = abac_contract.functions.registerUser(role, clearance_level).transact({'from': user_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("[SUCCESS] User registered successfully ✅")
    except Exception as e:
        print(f"[ERROR] Failed to register user: {e}")

# Function to Retrieve User Attributes
def get_user(user_address):
    try:
        print(f"[INFO] Fetching user attributes for {user_address}...")
        user_data = abac_contract.functions.getUser(user_address).call()
        print(f"[DATA] User Role: {user_data[0]}, Clearance Level: {user_data[1]}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch user attributes: {e}")

# Function to Check Access Control
def check_access(user_address, resource_id):
    try:
        print(f"[INFO] Checking access for {user_address} on resource '{resource_id}'...")
        access_granted = abac_contract.functions.checkAccess(user_address, resource_id).call()
        if access_granted:
            print("[ACCESS GRANTED] ✅ User has access!")
        else:
            print("[ACCESS DENIED] ❌ User does not have access.")
    except Exception as e:
        print(f"[ERROR] Failed to check access: {e}")


# Run Test Cases
if __name__ == "__main__":
    # Test 1: Check if contract is deployed
    print(f"[TEST] Contract deployed at: {ABAC_ADDRESS}")

    # Test 2: Register a new user
    user_address = w3.eth.accounts[1]  # Use second account from Ganache
    register_user(user_address, "Manager", 3)

    # Test 3: Retrieve user attributes
    get_user(user_address)

    # Test 4: Check access control
    check_access(user_address, "Resource123")